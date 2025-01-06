import logging
from contextlib import contextmanager
from os import getcwd, path, remove
from pathlib import Path
from unittest.mock import patch
import pytest
from click.testing import CliRunner
import time_machine

from sqlmesh.cli.example_project import ProjectTemplate, init_example_project
from sqlmesh.cli.main import cli
from sqlmesh.core.context import Context
from sqlmesh.integrations.dlt import generate_dlt_models
from sqlmesh.utils.date import yesterday_ds

FREEZE_TIME = "2023-01-01 00:00:00 UTC"

pytestmark = pytest.mark.slow


@pytest.fixture(scope="session")
def runner() -> CliRunner:
    return CliRunner()


@contextmanager
def disable_logging():
    logging.disable(logging.CRITICAL)
    try:
        yield
    finally:
        logging.disable(logging.NOTSET)


def create_example_project(temp_dir) -> None:
    """
    Sets up CLI tests requiring a real SQLMesh project by:
        - Creating the SQLMesh example project in the temp_dir directory
        - Overwriting the config.yaml file so the duckdb database file will be created in the temp_dir directory
    """
    init_example_project(temp_dir, "duckdb")
    with open(temp_dir / "config.yaml", "w", encoding="utf-8") as f:
        f.write(
            f"""gateways:
  local:
    connection:
      type: duckdb
      database: {temp_dir}/db.db

default_gateway: local

model_defaults:
  dialect: duckdb

plan:
  no_prompts: false
"""
        )


def update_incremental_model(temp_dir) -> None:
    with open(temp_dir / "models" / "incremental_model.sql", "w", encoding="utf-8") as f:
        f.write(
            """
MODEL (
  name sqlmesh_example.incremental_model,
  kind INCREMENTAL_BY_TIME_RANGE (
    time_column event_date
  ),
  start '2020-01-01',
  cron '@daily',
  grain (id, event_date)
);

SELECT
  id,
  item_id,
  'a' as new_col,
  event_date,
FROM
  sqlmesh_example.seed_model
WHERE
  event_date between @start_date and @end_date
"""
        )


def update_full_model(temp_dir) -> None:
    with open(temp_dir / "models" / "full_model.sql", "w", encoding="utf-8") as f:
        f.write(
            """
MODEL (
  name sqlmesh_example.full_model,
  kind FULL,
  cron '@daily',
  grain item_id,
  audits (assert_positive_order_ids),
);

SELECT
  item_id + 1 as item_id,
  count(distinct id) AS num_orders,
FROM
  sqlmesh_example.incremental_model
GROUP BY item_id
"""
        )


def init_prod_and_backfill(runner, temp_dir) -> None:
    result = runner.invoke(
        cli, ["--log-file-dir", temp_dir, "--paths", temp_dir, "plan", "--auto-apply"]
    )
    assert_plan_success(result)
    assert path.exists(temp_dir / "db.db")


def assert_duckdb_test(result) -> None:
    assert "Successfully Ran 1 tests against duckdb" in result.output


def assert_new_env(result, new_env="prod", from_env="prod", initialize=True) -> None:
    assert (
        f"`{new_env}` environment will be initialized"
        if initialize
        else f"New environment `{new_env}` will be created from `{from_env}`"
    ) in result.output


def assert_model_versions_created(result) -> None:
    assert "All model versions have been created successfully" in result.output


def assert_model_batches_executed(result) -> None:
    assert "All model batches have been executed successfully" in result.output


def assert_target_env_updated(result) -> None:
    assert "The target environment has been updated successfully" in result.output


def assert_backfill_success(result) -> None:
    assert_model_versions_created(result)
    assert_model_batches_executed(result)
    assert_target_env_updated(result)


def assert_plan_success(result, new_env="prod", from_env="prod") -> None:
    assert result.exit_code == 0
    assert_duckdb_test(result)
    assert_new_env(result, new_env, from_env)
    assert_backfill_success(result)


def assert_virtual_update(result) -> None:
    assert "Virtual Update executed successfully" in result.output


def test_version(runner, tmp_path):
    from sqlmesh import __version__ as SQLMESH_VERSION

    result = runner.invoke(cli, ["--log-file-dir", tmp_path, "--version"])
    assert result.exit_code == 0
    assert SQLMESH_VERSION in result.output


def test_plan_no_config(runner, tmp_path):
    # Error if no SQLMesh project config is found
    result = runner.invoke(cli, ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan"])
    assert result.exit_code == 1
    assert "Error: SQLMesh project config could not be found" in result.output


def test_plan(runner, tmp_path):
    create_example_project(tmp_path)

    # Example project models have start dates, so there are no date prompts
    # for the `prod` environment.
    # Input: `y` to apply and backfill
    result = runner.invoke(
        cli, ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan"], input="y\n"
    )
    assert_plan_success(result)


def test_plan_skip_tests(runner, tmp_path):
    create_example_project(tmp_path)

    # Successful test run message should not appear with `--skip-tests`
    # Input: `y` to apply and backfill
    result = runner.invoke(
        cli, ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan", "--skip-tests"], input="y\n"
    )
    assert result.exit_code == 0
    assert "Successfully Ran 1 tests against duckdb" not in result.output
    assert_new_env(result)
    assert_backfill_success(result)


def test_plan_restate_model(runner, tmp_path):
    create_example_project(tmp_path)
    init_prod_and_backfill(runner, tmp_path)

    # plan with no changes and full_model restated
    # Input: enter for backfill start date prompt, enter for end date prompt, `y` to apply and backfill
    result = runner.invoke(
        cli,
        [
            "--log-file-dir",
            tmp_path,
            "--paths",
            tmp_path,
            "plan",
            "--restate-model",
            "sqlmesh_example.full_model",
        ],
        input="\n\ny\n",
    )
    assert result.exit_code == 0
    assert_duckdb_test(result)
    assert "No changes to plan: project files match the `prod` environment" in result.output
    assert "sqlmesh_example.full_model evaluated in" in result.output
    assert_backfill_success(result)


@pytest.mark.parametrize("flag", ["--skip-backfill", "--dry-run"])
def test_plan_skip_backfill(runner, tmp_path, flag):
    create_example_project(tmp_path)

    # plan for `prod` errors if `--skip-backfill` is passed without --no-gaps
    result = runner.invoke(cli, ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan", flag])
    assert result.exit_code == 1
    assert (
        "Error: When targeting the production environment either the backfill should not be skipped or the lack of data gaps should be enforced (--no-gaps flag)."
        in result.output
    )

    # plan executes virtual update without executing model batches
    # Input: `y` to perform virtual update
    result = runner.invoke(
        cli,
        ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan", flag, "--no-gaps"],
        input="y\n",
    )
    assert result.exit_code == 0
    assert_virtual_update(result)
    assert "All model batches have been executed successfully" not in result.output


def test_plan_auto_apply(runner, tmp_path):
    create_example_project(tmp_path)

    # plan for `prod` runs end-to-end with no user input with `--auto-apply`
    result = runner.invoke(
        cli, ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan", "--auto-apply"]
    )
    assert_plan_success(result)

    # confirm verbose output not present
    assert "sqlmesh_example.seed_model created" not in result.output
    assert "sqlmesh_example.seed_model promoted" not in result.output


def test_plan_verbose(runner, tmp_path):
    create_example_project(tmp_path)

    # Input: `y` to apply and backfill
    result = runner.invoke(
        cli, ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan", "--verbose"], input="y\n"
    )
    assert_plan_success(result)
    assert "sqlmesh_example.seed_model created" in result.output
    assert "sqlmesh_example.seed_model promoted" in result.output


def test_plan_dev(runner, tmp_path):
    create_example_project(tmp_path)

    # Input: enter for backfill start date prompt, enter for end date prompt, `y` to apply and backfill
    result = runner.invoke(
        cli, ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan", "dev"], input="\n\ny\n"
    )
    assert_plan_success(result, "dev")


def test_plan_dev_start_date(runner, tmp_path):
    create_example_project(tmp_path)

    # Input: enter for backfill end date prompt, `y` to apply and backfill
    result = runner.invoke(
        cli,
        ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan", "dev", "--start", "2023-01-01"],
        input="\ny\n",
    )
    assert_plan_success(result, "dev")
    assert "sqlmesh_example__dev.full_model: 2023-01-01" in result.output
    assert "sqlmesh_example__dev.incremental_model: 2023-01-01" in result.output


def test_plan_dev_end_date(runner, tmp_path):
    create_example_project(tmp_path)

    # Input: enter for backfill start date prompt, `y` to apply and backfill
    result = runner.invoke(
        cli,
        ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan", "dev", "--end", "2023-01-01"],
        input="\ny\n",
    )
    assert_plan_success(result, "dev")
    assert "sqlmesh_example__dev.full_model: 2020-01-01 - 2023-01-01" in result.output
    assert "sqlmesh_example__dev.incremental_model: 2020-01-01 - 2023-01-01" in result.output


def test_plan_dev_create_from_virtual(runner, tmp_path):
    create_example_project(tmp_path)

    # create dev environment and backfill
    runner.invoke(
        cli,
        [
            "--log-file-dir",
            tmp_path,
            "--paths",
            tmp_path,
            "plan",
            "dev",
            "--no-prompts",
            "--auto-apply",
        ],
    )

    # create dev2 environment from dev environment
    # Input: `y` to apply and virtual update
    result = runner.invoke(
        cli,
        [
            "--log-file-dir",
            tmp_path,
            "--paths",
            tmp_path,
            "plan",
            "dev2",
            "--create-from",
            "dev",
            "--include-unmodified",
        ],
        input="y\n",
    )
    assert result.exit_code == 0
    assert_new_env(result, "dev2", "dev", initialize=False)
    assert_model_versions_created(result)
    assert_target_env_updated(result)
    assert_virtual_update(result)


def test_plan_dev_create_from(runner, tmp_path):
    create_example_project(tmp_path)

    # create dev environment and backfill
    runner.invoke(
        cli,
        [
            "--log-file-dir",
            tmp_path,
            "--paths",
            tmp_path,
            "plan",
            "dev",
            "--no-prompts",
            "--auto-apply",
        ],
    )
    # make model change
    update_incremental_model(tmp_path)

    # create dev2 environment from dev
    result = runner.invoke(
        cli,
        [
            "--log-file-dir",
            tmp_path,
            "--paths",
            tmp_path,
            "plan",
            "dev2",
            "--create-from",
            "dev",
            "--no-prompts",
            "--auto-apply",
        ],
    )

    assert result.exit_code == 0
    assert_new_env(result, "dev2", "dev", initialize=False)
    assert "Differences from the `dev` environment:" in result.output


def test_plan_dev_bad_create_from(runner, tmp_path):
    create_example_project(tmp_path)

    # create dev environment and backfill
    runner.invoke(
        cli,
        [
            "--log-file-dir",
            tmp_path,
            "--paths",
            tmp_path,
            "plan",
            "dev",
            "--no-prompts",
            "--auto-apply",
        ],
    )
    # make model change
    update_incremental_model(tmp_path)

    # create dev2 environment from non-existent dev3
    logger = logging.getLogger("sqlmesh.core.context_diff")
    with patch.object(logger, "warning") as mock_logger:
        result = runner.invoke(
            cli,
            [
                "--log-file-dir",
                tmp_path,
                "--paths",
                tmp_path,
                "plan",
                "dev2",
                "--create-from",
                "dev3",
                "--no-prompts",
                "--auto-apply",
            ],
        )

        assert result.exit_code == 0
        assert_new_env(result, "dev2", "dev")
        assert (
            mock_logger.call_args[0][0]
            == "The environment name 'dev3' was passed to the `plan` command's `--create-from` argument, but 'dev3' does not exist. Initializing new environment 'dev2' from scratch."
        )


def test_plan_dev_no_prompts(runner, tmp_path):
    create_example_project(tmp_path)

    # plan for non-prod environment doesn't prompt for dates but prompts to apply
    result = runner.invoke(
        cli, ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan", "dev", "--no-prompts"]
    )
    assert "Apply - Backfill Tables [y/n]: " in result.output
    assert "All model versions have been created successfully" not in result.output
    assert "All model batches have been executed successfully" not in result.output
    assert "The target environment has been updated successfully" not in result.output


def test_plan_dev_auto_apply(runner, tmp_path):
    create_example_project(tmp_path)

    # Input: enter for backfill start date prompt, enter for end date prompt
    result = runner.invoke(
        cli,
        ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan", "dev", "--auto-apply"],
        input="\n\n",
    )
    assert_plan_success(result, "dev")


def test_plan_dev_no_changes(runner, tmp_path):
    create_example_project(tmp_path)
    init_prod_and_backfill(runner, tmp_path)

    # Error if no changes made and `--include-unmodified` is not passed
    result = runner.invoke(cli, ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan", "dev"])
    assert result.exit_code == 1
    assert (
        "Error: Creating a new environment requires a change, but project files match the `prod` environment. Make a change or use the --include-unmodified flag to create a new environment without changes."
        in result.output
    )

    # No error if no changes made and `--include-unmodified` is passed
    # Input: `y` to apply and virtual update
    result = runner.invoke(
        cli,
        ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan", "dev", "--include-unmodified"],
        input="y\n",
    )
    assert result.exit_code == 0
    assert_new_env(result, "dev", initialize=False)
    assert_target_env_updated(result)
    assert_virtual_update(result)


def test_plan_nonbreaking(runner, tmp_path):
    create_example_project(tmp_path)
    init_prod_and_backfill(runner, tmp_path)

    update_incremental_model(tmp_path)

    # Input: `y` to apply and backfill
    result = runner.invoke(
        cli, ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan"], input="y\n"
    )
    assert result.exit_code == 0
    assert "Differences from the `prod` environment" in result.output
    assert "+  'a' AS new_col" in result.output
    assert "Directly Modified: sqlmesh_example.incremental_model (Non-breaking)" in result.output
    assert "sqlmesh_example.full_model (Indirect Non-breaking)" in result.output
    assert "sqlmesh_example.incremental_model evaluated in" in result.output
    assert "sqlmesh_example.full_model evaluated in" not in result.output
    assert_backfill_success(result)


def test_plan_nonbreaking_noautocategorization(runner, tmp_path):
    create_example_project(tmp_path)
    init_prod_and_backfill(runner, tmp_path)

    update_incremental_model(tmp_path)

    # Input: `2` to classify change as non-breaking, `y` to apply and backfill
    result = runner.invoke(
        cli,
        ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan", "--no-auto-categorization"],
        input="2\ny\n",
    )
    assert result.exit_code == 0
    assert (
        "[1] [Breaking] Backfill sqlmesh_example.incremental_model and indirectly \nmodified children"
        in result.output
    )
    assert (
        "[2] [Non-breaking] Backfill sqlmesh_example.incremental_model but not indirectly\nmodified children"
        in result.output
    )
    assert_backfill_success(result)


def test_plan_nonbreaking_nodiff(runner, tmp_path):
    create_example_project(tmp_path)
    init_prod_and_backfill(runner, tmp_path)

    update_incremental_model(tmp_path)

    # Input: `y` to apply and backfill
    result = runner.invoke(
        cli, ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan", "--no-diff"], input="y\n"
    )
    assert result.exit_code == 0
    assert "+  'a' AS new_col" not in result.output
    assert_backfill_success(result)


def test_plan_breaking(runner, tmp_path):
    create_example_project(tmp_path)
    init_prod_and_backfill(runner, tmp_path)

    update_full_model(tmp_path)

    # full_model change makes test fail, so we pass `--skip-tests`
    # Input: `y` to apply and backfill
    result = runner.invoke(
        cli, ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan", "--skip-tests"], input="y\n"
    )
    assert result.exit_code == 0
    assert "+  item_id + 1 AS item_id," in result.output
    assert "Directly Modified: sqlmesh_example.full_model (Breaking)" in result.output
    assert "sqlmesh_example.full_model evaluated in" in result.output
    assert "sqlmesh_example.incremental_model evaluated in" not in result.output
    assert_backfill_success(result)


def test_plan_dev_select(runner, tmp_path):
    create_example_project(tmp_path)
    init_prod_and_backfill(runner, tmp_path)

    update_incremental_model(tmp_path)
    update_full_model(tmp_path)

    # full_model change makes test fail, so we pass `--skip-tests`
    # Input: enter for backfill start date prompt, enter for end date prompt, `y` to apply and backfill
    result = runner.invoke(
        cli,
        [
            "--log-file-dir",
            tmp_path,
            "--paths",
            tmp_path,
            "plan",
            "dev",
            "--skip-tests",
            "--select-model",
            "sqlmesh_example.incremental_model",
        ],
        input="\n\ny\n",
    )
    assert result.exit_code == 0
    # incremental_model diff present
    assert "+  'a' AS new_col" in result.output
    assert (
        "Directly Modified: sqlmesh_example__dev.incremental_model (Non-breaking)" in result.output
    )
    # full_model diff not present
    assert "+  item_id + 1 AS item_id," not in result.output
    assert "Directly Modified: sqlmesh_example__dev.full_model (Breaking)" not in result.output
    # only incremental_model backfilled
    assert "sqlmesh_example__dev.incremental_model evaluated in" in result.output
    assert "sqlmesh_example__dev.full_model evaluated in" not in result.output
    assert_backfill_success(result)


def test_plan_dev_backfill(runner, tmp_path):
    create_example_project(tmp_path)
    init_prod_and_backfill(runner, tmp_path)

    update_incremental_model(tmp_path)
    update_full_model(tmp_path)

    # full_model change makes test fail, so we pass `--skip-tests`
    # Input: enter for backfill start date prompt, enter for end date prompt, `y` to apply and backfill
    result = runner.invoke(
        cli,
        [
            "--log-file-dir",
            tmp_path,
            "--paths",
            tmp_path,
            "plan",
            "dev",
            "--skip-tests",
            "--backfill-model",
            "sqlmesh_example.incremental_model",
        ],
        input="\n\ny\n",
    )
    assert result.exit_code == 0
    assert_new_env(result, "dev", initialize=False)
    # both model diffs present
    assert "+  item_id + 1 AS item_id," in result.output
    assert "Directly Modified: sqlmesh_example__dev.full_model (Breaking)" in result.output
    assert "+  'a' AS new_col" in result.output
    assert (
        "Directly Modified: sqlmesh_example__dev.incremental_model (Non-breaking)" in result.output
    )
    # only incremental_model backfilled
    assert "sqlmesh_example__dev.incremental_model evaluated in" in result.output
    assert "sqlmesh_example__dev.full_model evaluated in" not in result.output
    assert_backfill_success(result)


def test_run_no_prod(runner, tmp_path):
    create_example_project(tmp_path)

    # Error if no env specified and `prod` doesn't exist
    result = runner.invoke(cli, ["--log-file-dir", tmp_path, "--paths", tmp_path, "run"])
    assert result.exit_code == 1
    assert "Error: Environment 'prod' was not found." in result.output


@pytest.mark.parametrize("flag", ["--skip-backfill", "--dry-run"])
@time_machine.travel(FREEZE_TIME)
def test_run_dev(runner, tmp_path, flag):
    create_example_project(tmp_path)

    # Create dev environment but DO NOT backfill
    # Input: `y` for virtual update
    runner.invoke(
        cli,
        ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan", "dev", flag],
        input="y\n",
    )

    # Confirm backfill occurs when we run non-backfilled dev env
    result = runner.invoke(cli, ["--log-file-dir", tmp_path, "--paths", tmp_path, "run", "dev"])
    assert result.exit_code == 0
    assert_model_batches_executed(result)


@time_machine.travel(FREEZE_TIME)
def test_run_cron_not_elapsed(runner, tmp_path, caplog):
    create_example_project(tmp_path)
    init_prod_and_backfill(runner, tmp_path)

    # No error if `prod` environment exists and cron has not elapsed
    with disable_logging():
        result = runner.invoke(cli, ["--log-file-dir", tmp_path, "--paths", tmp_path, "run"])
    assert result.exit_code == 0

    assert (
        "No models are ready to run. Please wait until a model `cron` interval has \nelapsed.\n\nNext run will be ready at "
        in result.output.strip()
    )


def test_run_cron_elapsed(runner, tmp_path):
    create_example_project(tmp_path)

    # Create and backfill `prod` environment
    with time_machine.travel("2023-01-01 23:59:00 UTC", tick=False) as traveler:
        runner = CliRunner()
        init_prod_and_backfill(runner, tmp_path)

        # Run `prod` environment with daily cron elapsed
        traveler.move_to("2023-01-02 00:01:00 UTC")
        result = runner.invoke(cli, ["--log-file-dir", tmp_path, "--paths", tmp_path, "run"])

    assert result.exit_code == 0
    assert_model_batches_executed(result)


def test_clean(runner, tmp_path):
    # Create and backfill `prod` environment
    create_example_project(tmp_path)
    init_prod_and_backfill(runner, tmp_path)

    # Confirm cache exists
    cache_path = Path(tmp_path) / ".cache"
    assert cache_path.exists()
    assert len(list(cache_path.iterdir())) > 0

    # Invoke the clean command
    result = runner.invoke(cli, ["--log-file-dir", tmp_path, "--paths", tmp_path, "clean"])

    # Confirm cache was cleared
    assert result.exit_code == 0
    assert not cache_path.exists()


def test_table_name(runner, tmp_path):
    # Create and backfill `prod` environment
    create_example_project(tmp_path)
    init_prod_and_backfill(runner, tmp_path)
    with disable_logging():
        result = runner.invoke(
            cli,
            [
                "--log-file-dir",
                tmp_path,
                "--paths",
                tmp_path,
                "table_name",
                "sqlmesh_example.full_model",
            ],
        )
    assert result.exit_code == 0
    assert result.output.startswith("db.sqlmesh__sqlmesh_example.sqlmesh_example__full_model__")


def test_info_on_new_project_does_not_create_state_sync(runner, tmp_path):
    create_example_project(tmp_path)

    # Invoke the info command
    result = runner.invoke(cli, ["--log-file-dir", tmp_path, "--paths", tmp_path, "info"])
    assert result.exit_code == 0

    context = Context(paths=tmp_path)

    # Confirm that the state sync tables haven't been created
    assert not context.engine_adapter.table_exists("sqlmesh._snapshots")
    assert not context.engine_adapter.table_exists("sqlmesh._environments")
    assert not context.engine_adapter.table_exists("sqlmesh._intervals")
    assert not context.engine_adapter.table_exists("sqlmesh._plan_dags")
    assert not context.engine_adapter.table_exists("sqlmesh._versions")


def test_dlt_pipeline_errors(runner, tmp_path):
    # Error if no pipeline is provided
    result = runner.invoke(cli, ["--paths", tmp_path, "init", "-t", "dlt", "duckdb"])
    assert (
        "Error: DLT pipeline is a required argument to generate a SQLMesh project from DLT"
        in result.output
    )

    # Error if the pipeline provided is not correct
    result = runner.invoke(
        cli,
        ["--paths", tmp_path, "init", "-t", "dlt", "--dlt-pipeline", "missing_pipeline", "duckdb"],
    )
    assert "Error: Could not attach to pipeline" in result.output


def test_plan_dlt(runner, tmp_path):
    root_dir = path.abspath(getcwd())
    pipeline_path = root_dir + "/examples/sushi_dlt/sushi_pipeline.py"
    with open(pipeline_path) as file:
        exec(file.read())

    dataset_path = root_dir + "/sushi.duckdb"
    init_example_project(tmp_path, "duckdb", ProjectTemplate.DLT, "sushi")

    expected_config = f"""gateways:
  local:
    connection:
      type: duckdb
      database: {dataset_path}

default_gateway: local

model_defaults:
  dialect: duckdb
  start: {yesterday_ds()}
"""

    with open(tmp_path / "config.yaml") as file:
        config = file.read()

    expected_incremental_model = """MODEL (
  name sushi_dataset_sqlmesh.incremental_sushi_types,
  kind INCREMENTAL_BY_TIME_RANGE (
    time_column _dlt_load_time,
  ),
  grain (id),
);

SELECT
  CAST(c.id AS BIGINT) AS id,
  CAST(c.name AS TEXT) AS name,
  CAST(c._dlt_load_id AS TEXT) AS _dlt_load_id,
  CAST(c._dlt_id AS TEXT) AS _dlt_id,
  TO_TIMESTAMP(CAST(c._dlt_load_id AS DOUBLE)) as _dlt_load_time
FROM
  sushi_dataset.sushi_types as c
WHERE
  TO_TIMESTAMP(CAST(c._dlt_load_id AS DOUBLE)) BETWEEN @start_ds AND @end_ds
"""

    dlt_sushi_types_model_path = tmp_path / "models/incremental_sushi_types.sql"
    dlt_loads_model_path = tmp_path / "models/incremental__dlt_loads.sql"
    dlt_waiters_model_path = tmp_path / "models/incremental_waiters.sql"
    dlt_sushi_fillings_model_path = tmp_path / "models/incremental_sushi_menu__fillings.sql"
    dlt_sushi_twice_nested_model_path = (
        tmp_path / "models/incremental_sushi_menu__details__ingredients.sql"
    )

    with open(dlt_sushi_types_model_path) as file:
        incremental_model = file.read()

    expected_dlt_loads_model = """MODEL (
  name sushi_dataset_sqlmesh.incremental__dlt_loads,
  kind INCREMENTAL_BY_TIME_RANGE (
    time_column _dlt_load_time,
  ),
);

SELECT
  CAST(c.load_id AS TEXT) AS load_id,
  CAST(c.schema_name AS TEXT) AS schema_name,
  CAST(c.status AS BIGINT) AS status,
  CAST(c.inserted_at AS TIMESTAMP) AS inserted_at,
  CAST(c.schema_version_hash AS TEXT) AS schema_version_hash,
  TO_TIMESTAMP(CAST(c.load_id AS DOUBLE)) as _dlt_load_time
FROM
  sushi_dataset._dlt_loads as c
WHERE
  TO_TIMESTAMP(CAST(c.load_id AS DOUBLE)) BETWEEN @start_ds AND @end_ds
"""

    with open(dlt_loads_model_path) as file:
        dlt_loads_model = file.read()

    expected_nested_fillings_model = """MODEL (
  name sushi_dataset_sqlmesh.incremental_sushi_menu__fillings,
  kind INCREMENTAL_BY_TIME_RANGE (
    time_column _dlt_load_time,
  ),
);

SELECT
  CAST(c.value AS TEXT) AS value,
  CAST(c._dlt_root_id AS TEXT) AS _dlt_root_id,
  CAST(c._dlt_parent_id AS TEXT) AS _dlt_parent_id,
  CAST(c._dlt_list_idx AS BIGINT) AS _dlt_list_idx,
  CAST(c._dlt_id AS TEXT) AS _dlt_id,
  TO_TIMESTAMP(CAST(p._dlt_load_id AS DOUBLE)) as _dlt_load_time
FROM
  sushi_dataset.sushi_menu__fillings as c
JOIN
  sushi_dataset.sushi_menu as p
ON
  c._dlt_parent_id = p._dlt_id
WHERE
  TO_TIMESTAMP(CAST(p._dlt_load_id AS DOUBLE)) BETWEEN @start_ds AND @end_ds
"""

    with open(dlt_sushi_fillings_model_path) as file:
        nested_model = file.read()

    # Validate generated config and models
    assert config == expected_config
    assert dlt_loads_model_path.exists()
    assert dlt_sushi_types_model_path.exists()
    assert dlt_waiters_model_path.exists()
    assert dlt_sushi_fillings_model_path.exists()
    assert dlt_sushi_twice_nested_model_path.exists()
    assert dlt_loads_model == expected_dlt_loads_model
    assert incremental_model == expected_incremental_model
    assert nested_model == expected_nested_fillings_model

    # Plan prod and backfill
    result = runner.invoke(
        cli, ["--log-file-dir", tmp_path, "--paths", tmp_path, "plan", "--auto-apply"]
    )

    assert result.exit_code == 0
    assert_backfill_success(result)

    # Remove and update with missing model
    remove(dlt_waiters_model_path)
    assert not dlt_waiters_model_path.exists()

    # Update with force = False will generate only the missing model
    context = Context(paths=tmp_path)
    assert generate_dlt_models(context, "sushi", [], False) == [
        "sushi_dataset_sqlmesh.incremental_waiters"
    ]
    assert dlt_waiters_model_path.exists()

    # Remove all models
    remove(dlt_waiters_model_path)
    remove(dlt_loads_model_path)
    remove(dlt_sushi_types_model_path)
    remove(dlt_sushi_fillings_model_path)
    remove(dlt_sushi_twice_nested_model_path)

    # Update to generate a specific model: sushi_types
    assert generate_dlt_models(context, "sushi", ["sushi_types"], False) == [
        "sushi_dataset_sqlmesh.incremental_sushi_types"
    ]

    # Only the sushi_types should be generated now
    assert not dlt_waiters_model_path.exists()
    assert not dlt_loads_model_path.exists()
    assert not dlt_sushi_fillings_model_path.exists()
    assert not dlt_sushi_twice_nested_model_path.exists()
    assert dlt_sushi_types_model_path.exists()

    # Update with force = True will generate all models and overwrite existing ones
    generate_dlt_models(context, "sushi", [], True)
    assert dlt_loads_model_path.exists()
    assert dlt_sushi_types_model_path.exists()
    assert dlt_waiters_model_path.exists()
    assert dlt_sushi_fillings_model_path.exists()
    assert dlt_sushi_twice_nested_model_path.exists()

    remove(dataset_path)

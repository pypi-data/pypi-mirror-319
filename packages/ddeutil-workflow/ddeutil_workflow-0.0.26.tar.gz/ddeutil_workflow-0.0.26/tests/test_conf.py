import json
import os
import shutil
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo

import pytest
import toml
import yaml
from ddeutil.workflow.conf import Config, Loader, SimLoad
from ddeutil.workflow.scheduler import Schedule
from ddeutil.workflow.workflow import Workflow


def test_config():
    with mock.patch.object(Config, "max_job_parallel", -1):
        with pytest.raises(ValueError):
            Config()

    with mock.patch.object(Config, "stop_boundary_delta_str", "{"):
        with pytest.raises(ValueError):
            Config()

    conf = Config()
    os.environ["WORKFLOW_CORE_TIMEZONE"] = "Asia/Bangkok"
    conf = conf.refresh_dotenv()
    assert conf.tz == ZoneInfo("Asia/Bangkok")


@pytest.fixture(scope="module")
def target_path(test_path):
    target_p = test_path / "test_simple_load"
    target_p.mkdir(exist_ok=True)

    with (target_p / "test_simple_file.json").open(mode="w") as f:
        json.dump({"foo": "bar"}, f)

    with (target_p / "test_simple_file.toml").open(mode="w") as f:
        toml.dump({"foo": "bar"}, f)

    yield target_p

    shutil.rmtree(target_p)


def test_simple_load(target_path: Path):
    with mock.patch.object(Config, "conf_path", target_path):
        with pytest.raises(ValueError):
            SimLoad("test_simple_load_raise", Config())


def test_simple_load_finds(target_path: Path):
    dummy_file: Path = target_path / "test_simple_file.yaml"
    with dummy_file.open(mode="w") as f:
        yaml.dump(
            {
                "test_simple_load_config": {
                    "type": "Config",
                    "foo": "bar",
                },
                "test_simple_load": {"type": "Workflow"},
            },
            f,
        )

    with mock.patch.object(Config, "conf_path", target_path):
        assert [
            (
                "test_simple_load_config",
                {"type": "Config", "foo": "bar"},
            )
        ] == list(SimLoad.finds(Config, Config()))
        assert [
            (
                "test_simple_load_config",
                {"type": "Config"},
            )
        ] == list(SimLoad.finds(Config, Config(), included="type"))
        assert [] == list(
            SimLoad.finds(Config, Config(), excluded="test_simple_load_config")
        )

    dummy_file.unlink()


def test_simple_load_finds_raise(target_path: Path):
    dummy_file: Path = target_path / "test_simple_file_raise.yaml"
    with dummy_file.open(mode="w") as f:
        yaml.dump(
            {
                "test_simple_load_config": {
                    "foo": "bar",
                },
                "test_simple_load": {"type": "Workflow"},
            },
            f,
        )

    with mock.patch.object(Config, "conf_path", target_path):
        with pytest.raises(ValueError):
            _ = SimLoad("test_simple_load_config", Config()).type


def test_loader_find_schedule():
    for finding in Loader.finds(Schedule, excluded=[]):
        print(finding)

    for finding in Loader.finds(
        Schedule,
        excluded=[
            "schedule-common-wf",
            "schedule-multi-on-wf",
            "schedule-every-minute-wf",
            "schedule-every-minute-wf-parallel",
        ],
    ):
        print(finding[0])


def test_loader_find_workflow():
    for finding in Loader.finds(Workflow, excluded=[]):
        print(finding)

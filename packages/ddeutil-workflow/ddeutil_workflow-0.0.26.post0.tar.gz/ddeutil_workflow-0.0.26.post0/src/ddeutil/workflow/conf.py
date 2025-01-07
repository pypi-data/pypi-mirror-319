# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import json
import logging
import os
from abc import ABC, abstractmethod
from collections.abc import Iterator
from datetime import datetime, timedelta
from functools import cached_property, lru_cache
from pathlib import Path
from typing import ClassVar, Optional, TypeVar, Union
from zoneinfo import ZoneInfo

from ddeutil.core import str2bool
from ddeutil.io import YamlFlResolve
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic.functional_validators import model_validator
from typing_extensions import Self

from .__types import DictData, TupleStr

AnyModel = TypeVar("AnyModel", bound=BaseModel)
AnyModelType = type[AnyModel]

load_dotenv()

env = os.getenv

__all__: TupleStr = (
    "get_logger",
    "Config",
    "SimLoad",
    "Loader",
    "config",
    "logger",
    "FileLog",
    "SQLiteLog",
    "Log",
)


@lru_cache
def get_logger(name: str):
    """Return logger object with an input module name.

    :param name: A module name that want to log.
    """
    lg = logging.getLogger(name)
    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s.%(msecs)03d (%(name)-10s, %(process)-5d, "
            "%(thread)-5d) [%(levelname)-7s] %(message)-120s "
            "(%(filename)s:%(lineno)s)"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    lg.addHandler(stream)

    lg.setLevel(logging.DEBUG if config.debug else logging.INFO)
    return lg


class Config:
    """Config object for keeping application configuration on current session
    without changing when if the application still running.
    """

    # NOTE: Core
    root_path: Path = Path(os.getenv("WORKFLOW_ROOT_PATH", "."))
    tz: ZoneInfo = ZoneInfo(env("WORKFLOW_CORE_TIMEZONE", "UTC"))
    gen_id_simple_mode: bool = str2bool(
        os.getenv("WORKFLOW_CORE_GENERATE_ID_SIMPLE_MODE", "true")
    )

    # NOTE: Register
    regis_hook_str: str = os.getenv(
        "WORKFLOW_CORE_REGISTRY", "src,src.ddeutil.workflow,tests,tests.utils"
    )
    regis_filter_str: str = os.getenv(
        "WORKFLOW_CORE_REGISTRY_FILTER", "ddeutil.workflow.utils"
    )

    # NOTE: Logging
    debug: bool = str2bool(os.getenv("WORKFLOW_LOG_DEBUG_MODE", "true"))
    enable_write_log: bool = str2bool(
        os.getenv("WORKFLOW_LOG_ENABLE_WRITE", "false")
    )
    log_path: Path = Path(os.getenv("WORKFLOW_LOG_PATH", "./logs"))

    # NOTE: Stage
    stage_raise_error: bool = str2bool(
        env("WORKFLOW_CORE_STAGE_RAISE_ERROR", "false")
    )
    stage_default_id: bool = str2bool(
        env("WORKFLOW_CORE_STAGE_DEFAULT_ID", "false")
    )

    # NOTE: Job
    job_raise_error: bool = str2bool(
        env("WORKFLOW_CORE_JOB_RAISE_ERROR", "true")
    )
    job_default_id: bool = str2bool(
        env("WORKFLOW_CORE_JOB_DEFAULT_ID", "false")
    )

    # NOTE: Workflow
    max_job_parallel: int = int(env("WORKFLOW_CORE_MAX_JOB_PARALLEL", "2"))
    max_job_exec_timeout: int = int(
        env("WORKFLOW_CORE_MAX_JOB_EXEC_TIMEOUT", "600")
    )
    max_poking_pool_worker: int = int(
        os.getenv("WORKFLOW_CORE_MAX_NUM_POKING", "4")
    )
    max_on_per_workflow: int = int(
        env("WORKFLOW_CORE_MAX_CRON_PER_WORKFLOW", "5")
    )
    max_queue_complete_hist: int = int(
        os.getenv("WORKFLOW_CORE_MAX_QUEUE_COMPLETE_HIST", "16")
    )

    # NOTE: Schedule App
    max_schedule_process: int = int(env("WORKFLOW_APP_MAX_PROCESS", "2"))
    max_schedule_per_process: int = int(
        env("WORKFLOW_APP_MAX_SCHEDULE_PER_PROCESS", "100")
    )
    stop_boundary_delta_str: str = env(
        "WORKFLOW_APP_STOP_BOUNDARY_DELTA", '{"minutes": 5, "seconds": 20}'
    )

    # NOTE: API
    prefix_path: str = env("WORKFLOW_API_PREFIX_PATH", "/api/v1")
    enable_route_workflow: bool = str2bool(
        env("WORKFLOW_API_ENABLE_ROUTE_WORKFLOW", "true")
    )
    enable_route_schedule: bool = str2bool(
        env("WORKFLOW_API_ENABLE_ROUTE_SCHEDULE", "true")
    )

    def __init__(self) -> None:
        # VALIDATE: the MAX_JOB_PARALLEL value should not less than 0.
        if self.max_job_parallel < 0:
            raise ValueError(
                f"``MAX_JOB_PARALLEL`` should more than 0 but got "
                f"{self.max_job_parallel}."
            )

        try:
            self.stop_boundary_delta: timedelta = timedelta(
                **json.loads(self.stop_boundary_delta_str)
            )
        except Exception as err:
            raise ValueError(
                "Config ``WORKFLOW_APP_STOP_BOUNDARY_DELTA`` can not parsing to"
                f"timedelta with {self.stop_boundary_delta_str}."
            ) from err

    @property
    def conf_path(self) -> Path:
        """Config path that use root_path class argument for this construction.

        :rtype: Path
        """
        return self.root_path / os.getenv("WORKFLOW_CORE_PATH_CONF", "conf")

    @property
    def regis_hook(self) -> list[str]:
        return [r.strip() for r in self.regis_hook_str.split(",")]

    @property
    def regis_filter(self) -> list[str]:
        return [r.strip() for r in self.regis_filter_str.split(",")]


class SimLoad:
    """Simple Load Object that will search config data by given some identity
    value like name of workflow or on.

    :param name: A name of config data that will read by Yaml Loader object.
    :param conf: A Params model object.
    :param externals: An external parameters

    Noted:

        The config data should have ``type`` key for modeling validation that
    make this loader know what is config should to do pass to.

        ... <identity-key>:
        ...     type: <importable-object>
        ...     <key-data>: <value-data>
        ...     ...

    """

    def __init__(
        self,
        name: str,
        conf: Config,
        externals: DictData | None = None,
    ) -> None:
        self.data: DictData = {}
        for file in conf.conf_path.rglob("*"):
            if not file.is_file():
                continue

            if data := self.filter_suffix(
                file,
                name,
            ):
                self.data = data

        # VALIDATE: check the data that reading should not empty.
        if not self.data:
            raise ValueError(f"Config {name!r} does not found on conf path")

        self.conf: Config = conf
        self.externals: DictData = externals or {}
        self.data.update(self.externals)

    @classmethod
    def finds(
        cls,
        obj: object,
        conf: Config,
        *,
        included: list[str] | None = None,
        excluded: list[str] | None = None,
    ) -> Iterator[tuple[str, DictData]]:
        """Find all data that match with object type in config path. This class
        method can use include and exclude list of identity name for filter and
        adds-on.

        :param obj: A object that want to validate matching before return.
        :param conf: A config object.
        :param included:
        :param excluded:

        :rtype: Iterator[tuple[str, DictData]]
        """
        exclude: list[str] = excluded or []
        for file in conf.conf_path.rglob("*"):

            if not file.is_file():
                continue

            for key, data in cls.filter_suffix(file).items():

                if key in exclude:
                    continue

                if data["type"] == obj.__name__:
                    yield key, (
                        {k: data[k] for k in data if k in included}
                        if included
                        else data
                    )

    @classmethod
    def filter_suffix(cls, file: Path, name: str | None = None) -> DictData:
        if any(file.suffix.endswith(s) for s in (".yml", ".yaml")):
            values: DictData = YamlFlResolve(file).read()
            return values.get(name, {}) if name else values
        return {}

    @cached_property
    def type(self) -> str:
        """Return object of string type which implement on any registry. The
        object type.

        :rtype: AnyModelType
        """
        if _typ := self.data.get("type"):
            return _typ
        raise ValueError(
            f"the 'type' value: {_typ} does not exists in config data."
        )


class Loader(SimLoad):
    """Loader Object that get the config `yaml` file from current path.

    :param name: A name of config data that will read by Yaml Loader object.
    :param externals: An external parameters
    """

    @classmethod
    def finds(
        cls,
        obj: object,
        *,
        included: list[str] | None = None,
        excluded: list[str] | None = None,
        **kwargs,
    ) -> Iterator[tuple[str, DictData]]:
        """Override the find class method from the Simple Loader object.

        :param obj: A object that want to validate matching before return.
        :param included:
        :param excluded:

        :rtype: Iterator[tuple[str, DictData]]
        """
        return super().finds(
            obj=obj, conf=Config(), included=included, excluded=excluded
        )

    def __init__(self, name: str, externals: DictData) -> None:
        super().__init__(name, conf=Config(), externals=externals)


config = Config()
logger = get_logger("ddeutil.workflow")


class BaseLog(BaseModel, ABC):
    """Base Log Pydantic Model with abstraction class property that implement
    only model fields. This model should to use with inherit to logging
    sub-class like file, sqlite, etc.
    """

    name: str = Field(description="A workflow name.")
    release: datetime = Field(description="A release datetime.")
    type: str = Field(description="A running type before logging.")
    context: DictData = Field(
        default_factory=dict,
        description=(
            "A context data that receive from a workflow execution result.",
        ),
    )
    parent_run_id: Optional[str] = Field(default=None)
    run_id: str
    update: datetime = Field(default_factory=datetime.now)

    @model_validator(mode="after")
    def __model_action(self) -> Self:
        """Do before the Log action with WORKFLOW_LOG_ENABLE_WRITE env variable.

        :rtype: Self
        """
        if config.enable_write_log:
            self.do_before()
        return self

    def do_before(self) -> None:  # pragma: no cov
        """To something before end up of initial log model."""

    @abstractmethod
    def save(self, excluded: list[str] | None) -> None:  # pragma: no cov
        """Save this model logging to target logging store."""
        raise NotImplementedError("Log should implement ``save`` method.")


class FileLog(BaseLog):
    """File Log Pydantic Model that use to saving log data from result of
    workflow execution. It inherit from BaseLog model that implement the
    ``self.save`` method for file.
    """

    filename_fmt: ClassVar[str] = (
        "workflow={name}/release={release:%Y%m%d%H%M%S}"
    )

    def do_before(self) -> None:
        """Create directory of release before saving log file."""
        self.pointer().mkdir(parents=True, exist_ok=True)

    @classmethod
    def find_logs(cls, name: str) -> Iterator[Self]:
        """Generate the logging data that found from logs path with specific a
        workflow name.

        :param name: A workflow name that want to search release logging data.

        :rtype: Iterator[Self]
        """
        pointer: Path = config.log_path / f"workflow={name}"
        if not pointer.exists():
            raise FileNotFoundError(f"Pointer: {pointer.absolute()}.")

        for file in pointer.glob("./release=*/*.log"):
            with file.open(mode="r", encoding="utf-8") as f:
                yield cls.model_validate(obj=json.load(f))

    @classmethod
    def find_log_with_release(
        cls,
        name: str,
        release: datetime | None = None,
    ) -> Self:
        """Return the logging data that found from logs path with specific
        workflow name and release values. If a release does not pass to an input
        argument, it will return the latest release from the current log path.

        :param name:
        :param release:

        :raise FileNotFoundError:
        :raise NotImplementedError:

        :rtype: Self
        """
        if release is None:
            raise NotImplementedError("Find latest log does not implement yet.")

        pointer: Path = (
            config.log_path / f"workflow={name}/release={release:%Y%m%d%H%M%S}"
        )
        if not pointer.exists():
            raise FileNotFoundError(
                f"Pointer: ./logs/workflow={name}/"
                f"release={release:%Y%m%d%H%M%S} does not found."
            )

        with max(pointer.glob("./*.log"), key=os.path.getctime).open(
            mode="r", encoding="utf-8"
        ) as f:
            return cls.model_validate(obj=json.load(f))

    @classmethod
    def is_pointed(cls, name: str, release: datetime) -> bool:
        """Check the release log already pointed or created at the destination
        log path.

        :param name: A workflow name.
        :param release: A release datetime.

        :rtype: bool
        :return: Return False if the release log was not pointed or created.
        """
        # NOTE: Return False if enable writing log flag does not set.
        if not config.enable_write_log:
            return False

        # NOTE: create pointer path that use the same logic of pointer method.
        pointer: Path = config.log_path / cls.filename_fmt.format(
            name=name, release=release
        )

        return pointer.exists()

    def pointer(self) -> Path:
        """Return release directory path that was generated from model data.

        :rtype: Path
        """
        return config.log_path / self.filename_fmt.format(
            name=self.name, release=self.release
        )

    def save(self, excluded: list[str] | None) -> Self:
        """Save logging data that receive a context data from a workflow
        execution result.

        :param excluded: An excluded list of key name that want to pass in the
            model_dump method.

        :rtype: Self
        """
        # NOTE: Check environ variable was set for real writing.
        if not config.enable_write_log:
            return self

        log_file: Path = self.pointer() / f"{self.run_id}.log"
        log_file.write_text(
            json.dumps(
                self.model_dump(exclude=excluded),
                default=str,
                indent=2,
            ),
            encoding="utf-8",
        )
        return self


class SQLiteLog(BaseLog):  # pragma: no cov

    def save(self, excluded: list[str] | None) -> None:
        raise NotImplementedError("SQLiteLog does not implement yet.")


Log = Union[
    FileLog,
    SQLiteLog,
]

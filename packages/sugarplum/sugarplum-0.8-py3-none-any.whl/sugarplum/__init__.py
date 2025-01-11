import os
from pathlib import Path
from typing import Any, NamedTuple

import yaml


class TestData(NamedTuple):
    data: str
    answer: int


def _get_file_path(year: int, day: int, filename: str) -> Path:
    return Path(os.environ["SUGARPLUM_BASE_PATH"]) / f"{year}/{day:02}/{filename}"


def get_input_data(year: int, day: int) -> str:
    with open(_get_file_path(year, day, "input.txt")) as f:
        return f.read()


def get_test_data(year: int, day: int, tag: str) -> TestData | list[TestData]:
    with open(_get_file_path(year, day, "tests.yaml")) as f:
        file_data: dict[str, Any] = yaml.safe_load(f)
    tagged_data = file_data[tag]
    if type(tagged_data) is list:
        return [TestData(entry["data"], entry["answer"]) for entry in tagged_data]
    elif type(tagged_data["data"]) is list:
        return TestData(
            "\n".join([x if x else "" for x in tagged_data["data"]]),
            tagged_data["answer"],
        )
    else:
        return TestData(tagged_data["data"], tagged_data["answer"])

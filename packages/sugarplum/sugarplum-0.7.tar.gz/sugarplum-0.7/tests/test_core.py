from pathlib import Path
from textwrap import dedent
from typing import Callable

import pytest

from sugarplum import TestData, get_input_data, get_test_data

YEAR: int = 2024
DAY: int = 24


@pytest.fixture(autouse=True)
def base_path(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SUGARPLUM_BASE_PATH", str(tmp_path))


@pytest.fixture(autouse=True)
def setup_dirs(tmp_path: Path) -> None:
    (tmp_path / str(YEAR)).mkdir()
    (tmp_path / f"{YEAR}/{DAY}").mkdir()


@pytest.fixture
def create_files(tmp_path: Path) -> Callable:
    def _create_files(data: list[tuple[str, str]]) -> None:
        for entry in data:
            with open(tmp_path / f"{YEAR}/{DAY}/{entry[0]}", "w") as f:
                f.write(str(entry[1]))

    return _create_files


def test_get_input_data(create_files: Callable) -> None:
    data: str = "North Pole"
    create_files([("input.txt", data)])

    assert get_input_data(YEAR, DAY) == data


def test_day_is_zero_padded(tmp_path: Path) -> None:
    data: str = "Santa Claus"
    day: int = 5
    (tmp_path / f"{YEAR}/{day:02}").mkdir()
    (tmp_path / f"{YEAR}/{day:02}/input.txt").write_text(data, encoding="utf-8")

    assert get_input_data(YEAR, day) == data


def test_getting_singular_test_data(create_files: Callable) -> None:
    expected: TestData = TestData("Santa Claus", 25)
    tag: str = "Dasher"
    compiled: str = dedent(
        f"""\
    {tag}:
        data: {expected.data}
        answer: {expected.answer}
    """
    )
    create_files([("tests.yaml", compiled)])

    assert get_test_data(YEAR, DAY, tag) == expected


def test_getting_test_data_that_needs_to_be_joined(create_files: Callable) -> None:
    data: list[str] = ["Santa Claus", "Kris Kringle"]
    expected: TestData = TestData("\n".join(data), 42)
    tag: str = "Dancer"
    compiled: str = dedent(
        f"""\
    {tag}:
        data:
            - {data[0]}
            - {data[1]}
        answer: {expected.answer}
    """
    )
    create_files([("tests.yaml", compiled)])

    assert get_test_data(YEAR, DAY, tag) == expected


def test_getting_parametrized_test_data(create_files: Callable) -> None:
    expected: list[TestData] = [
        TestData("Jingle Bells", 15),
        TestData("White Christmas", 73),
    ]
    tag: str = "Prancer"
    compiled: str = dedent(
        f"""\
    {tag}:
        - data: {expected[0].data}
          answer: {expected[0].answer}
        - data: {expected[1].data}
          answer: {expected[1].answer}
    """
    )
    create_files([("tests.yaml", compiled)])

    assert get_test_data(YEAR, DAY, tag) == expected

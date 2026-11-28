from collections.abc import Callable, Iterator
from dataclasses import fields, is_dataclass
from enum import Enum
from importlib import import_module
from inspect import Parameter, isfunction, signature
from pkgutil import walk_packages
from types import FunctionType, NoneType, UnionType
from typing import Union, get_args, get_origin, get_type_hints

import pytest

from bible_music import app
from bible_music.app import commands, views
from bible_music.domain.passage_plan import PermittedEnding, SongBoundaryPolicy
from bible_music.domain.take import AudioRevisionRef, Take
from bible_music.domain.take_review import (
    EvidenceSource,
    ListenerObservation,
    ObservedWord,
    TimeSpan,
    TimingPrecision,
)

VALUE_TYPES = (bool, int, str, NoneType, Ellipsis)
VALUE_CONTAINERS = (tuple, frozenset, Union, UnionType)
COMMAND_DOMAIN_VALUES = frozenset(
    {
        AudioRevisionRef,
        EvidenceSource,
        ListenerObservation,
        ObservedWord,
        PermittedEnding,
        SongBoundaryPolicy,
        TimeSpan,
        TimingPrecision,
    }
)


def public_use_cases() -> Iterator[FunctionType]:
    modules = (
        app,
        *(
            import_module(info.name)
            for info in walk_packages(app.__path__, f"{app.__name__}.")
        ),
    )
    for module in modules:
        for name, candidate in vars(module).items():
            if name.startswith("_"):
                continue
            if isfunction(candidate) and candidate.__module__ == module.__name__:
                yield candidate
            elif (
                isinstance(candidate, type) and candidate.__module__ == module.__name__
            ):
                method = vars(candidate).get("__call__")
                if isfunction(method):
                    yield method


def assert_value_fields(
    annotation: object, field_path: str, allowed: Callable[[type], bool]
) -> None:
    if annotation in VALUE_TYPES:
        return
    if get_origin(annotation) in VALUE_CONTAINERS:
        for argument in get_args(annotation):
            assert_value_fields(argument, field_path, allowed)
        return
    assert isinstance(annotation, type) and allowed(annotation), (
        f"{field_path} exposes an unapproved type {annotation!r}"
    )
    if issubclass(annotation, Enum):
        return
    assert is_dataclass(annotation) and annotation.__dataclass_params__.frozen, (
        f"{field_path} must use an immutable value"
    )
    field_types = get_type_hints(annotation)
    for field in fields(annotation):
        assert_value_fields(
            field_types[field.name], f"{field_path}.{field.name}", allowed
        )


def command_value(annotation: type) -> bool:
    return (
        annotation.__module__ == commands.__name__
        or annotation in COMMAND_DOMAIN_VALUES
    )


def view_value(annotation: type) -> bool:
    return annotation.__module__ == views.__name__


USE_CASES = tuple(public_use_cases())


def test_the_application_exposes_use_cases() -> None:
    assert USE_CASES


@pytest.mark.parametrize(
    "use_case", USE_CASES, ids=lambda use_case: use_case.__qualname__
)
def test_public_use_case_accepts_one_typed_command(use_case: FunctionType) -> None:
    parameters = tuple(signature(use_case).parameters.values())
    command_parameters = (
        parameters[1:] if use_case.__name__ == "__call__" else parameters
    )
    assert len(command_parameters) == 1
    (parameter,) = command_parameters
    assert parameter.kind is Parameter.POSITIONAL_OR_KEYWORD
    assert parameter.default is Parameter.empty
    command_type = get_type_hints(use_case).get(parameter.name)
    assert is_dataclass(command_type) and command_type.__module__ == commands.__name__
    assert_value_fields(
        command_type, f"{use_case.__qualname__}.{parameter.name}", command_value
    )


@pytest.mark.parametrize(
    "use_case", USE_CASES, ids=lambda use_case: use_case.__qualname__
)
def test_public_use_case_returns_an_app_owned_immutable_view(
    use_case: FunctionType,
) -> None:
    result_type = get_type_hints(use_case).get("return")
    assert is_dataclass(result_type), (
        f"{use_case.__qualname__} must return a typed view"
    )
    assert_value_fields(result_type, use_case.__qualname__, view_value)


def test_command_contract_rejects_a_frozen_aggregate_inside_a_collection() -> None:
    with pytest.raises(AssertionError, match="unapproved type .*Take"):
        assert_value_fields(tuple[Take, ...], "command.takes", command_value)

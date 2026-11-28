from collections.abc import Callable, Iterator
from dataclasses import fields, is_dataclass, make_dataclass
from enum import Enum
from importlib import import_module
from inspect import Parameter, Signature, isfunction, signature
from pkgutil import walk_packages
from types import FunctionType, ModuleType, NoneType, UnionType
from typing import Union, get_args, get_origin, get_type_hints, is_protocol

import pytest

from bible_music import app
from bible_music.app import mapping, ports, queries, views
from bible_music.app.ports import inbound, outbound
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
REQUEST_SUFFIXES = {
    f"{app.__name__}.commands": "Command",
    queries.__name__: "Query",
}
REQUEST_DOMAIN_VALUES = frozenset(
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


def use_case_modules() -> Iterator[ModuleType]:
    yield app
    support_packages = (mapping.__name__, ports.__name__)
    for info in walk_packages(app.__path__, f"{app.__name__}."):
        if any(
            info.name == package or info.name.startswith(f"{package}.")
            for package in support_packages
        ):
            continue
        yield import_module(info.name)


def public_use_cases() -> Iterator[FunctionType]:
    for module in use_case_modules():
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


def declared_ports(module: ModuleType) -> Iterator[type]:
    for name, candidate in vars(module).items():
        if (
            not name.startswith("_")
            and isinstance(candidate, type)
            and candidate.__module__ == module.__name__
        ):
            assert is_protocol(candidate), f"{name} must be a protocol"
            yield candidate


def public_signature(entry: FunctionType) -> Signature:
    declared = signature(entry)
    parameters = tuple(declared.parameters.values())
    if entry.__name__ == "__call__":
        parameters = parameters[1:]
    hints = get_type_hints(entry)
    return declared.replace(
        parameters=(
            parameter.replace(annotation=hints.get(parameter.name, Parameter.empty))
            for parameter in parameters
        ),
        return_annotation=hints.get("return", Signature.empty),
    )


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


def request_value(annotation: type) -> bool:
    return (
        annotation.__module__ in REQUEST_SUFFIXES or annotation in REQUEST_DOMAIN_VALUES
    )


def view_value(annotation: type) -> bool:
    return annotation.__module__ == views.__name__


def assert_request_type(annotation: object, path: str) -> None:
    assert isinstance(annotation, type) and is_dataclass(annotation), (
        f"{path} must be a command or query dataclass"
    )
    suffix = REQUEST_SUFFIXES.get(annotation.__module__)
    assert suffix and annotation.__name__.endswith(suffix), (
        f"{path} must use a Command from app.commands or a Query from app.queries"
    )
    assert_value_fields(annotation, path, request_value)


USE_CASES = tuple(public_use_cases())


def test_the_application_exposes_use_cases() -> None:
    assert USE_CASES


@pytest.mark.parametrize(
    "use_case", USE_CASES, ids=lambda use_case: use_case.__qualname__
)
def test_public_use_case_accepts_one_typed_request(use_case: FunctionType) -> None:
    parameters = public_signature(use_case).parameters
    assert len(parameters) == 1
    (parameter,) = parameters.values()
    assert parameter.kind is Parameter.POSITIONAL_OR_KEYWORD
    assert parameter.default is Parameter.empty
    assert_request_type(
        parameter.annotation, f"{use_case.__qualname__}.{parameter.name}"
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


def test_public_use_cases_match_their_inbound_port_signatures() -> None:
    port_signatures = set()
    for port in declared_ports(inbound):
        method = vars(port).get("__call__")
        assert isfunction(method), f"{port.__name__} must declare a callable contract"
        port_signatures.add(public_signature(method))

    use_case_signatures = {public_signature(use_case) for use_case in USE_CASES}
    assert use_case_signatures == port_signatures


def test_outbound_ports_are_protocols() -> None:
    assert tuple(declared_ports(outbound))


@pytest.mark.parametrize(("module", "suffix"), tuple(REQUEST_SUFFIXES.items()))
def test_request_contract_rejects_a_frozen_aggregate_inside_a_collection(
    module: str, suffix: str
) -> None:
    request_type = make_dataclass(
        f"InvalidTake{suffix}",
        [("takes", tuple[Take, ...])],
        frozen=True,
        module=module,
    )
    with pytest.raises(
        AssertionError, match=r"request\.takes exposes an unapproved type .*Take"
    ):
        assert_request_type(request_type, "request")

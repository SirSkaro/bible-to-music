from dataclasses import fields, is_dataclass
from enum import StrEnum
from importlib import import_module
from inspect import isfunction
from pkgutil import walk_packages
from types import NoneType, UnionType
from typing import Union, get_args, get_origin, get_type_hints

import pytest

from bible_music import app
from bible_music.app import views

VALUE_TYPES = (bool, int, str, NoneType, Ellipsis)
VIEW_CONTAINERS = (tuple, frozenset, Union, UnionType)


def public_use_cases():
    modules = (
        app,
        *(
            import_module(info.name)
            for info in walk_packages(app.__path__, f"{app.__name__}.")
        ),
    )
    for module in modules:
        for name, candidate in vars(module).items():
            if (
                not name.startswith("_")
                and isfunction(candidate)
                and candidate.__module__ == module.__name__
            ):
                yield pytest.param(candidate, id=f"{module.__name__}.{name}")


def assert_view_fields(annotation, field_path):
    if annotation in VALUE_TYPES:
        return
    if get_origin(annotation) in VIEW_CONTAINERS:
        for argument in get_args(annotation):
            assert_view_fields(argument, field_path)
        return
    assert isinstance(annotation, type) and annotation.__module__ == views.__name__, (
        f"{field_path} exposes {annotation!r} outside the application view contract"
    )
    if issubclass(annotation, StrEnum):
        return
    assert is_dataclass(annotation) and annotation.__dataclass_params__.frozen, (
        f"{field_path} must use an immutable application view"
    )
    field_types = get_type_hints(annotation)
    for field in fields(annotation):
        assert_view_fields(field_types[field.name], f"{field_path}.{field.name}")


@pytest.mark.parametrize("use_case", tuple(public_use_cases()))
def test_public_use_case_returns_an_app_owned_immutable_view(use_case):
    result_type = get_type_hints(use_case).get("return")
    assert is_dataclass(result_type), f"{use_case.__name__} must return a typed view"
    assert_view_fields(result_type, use_case.__name__)

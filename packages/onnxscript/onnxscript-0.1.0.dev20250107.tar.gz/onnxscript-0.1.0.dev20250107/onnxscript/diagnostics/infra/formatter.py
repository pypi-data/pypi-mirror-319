# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
from __future__ import annotations

import dataclasses
import json
import re
from typing import Any, Callable, Dict, List, Optional, Union

from onnxscript._internal import runtime_typing
from onnxscript.diagnostics.infra import sarif

# A list of types in the SARIF module to support pretty printing.
# This is solely for type annotation for the functions below.
_SarifClass = Union[
    sarif.SarifLog,
    sarif.Run,
    sarif.ReportingDescriptor,
    sarif.Result,
]


@runtime_typing.checked
def snake_case_to_camel_case(s: str) -> str:
    splits = s.split("_")
    if len(splits) <= 1:
        return s
    return "".join([splits[0], *map(str.capitalize, splits[1:])])


@runtime_typing.checked
def camel_case_to_snake_case(s: str) -> str:
    return re.sub(r"([A-Z])", r"_\1", s).lower()


@runtime_typing.checked
def kebab_case_to_snake_case(s: str) -> str:
    return s.replace("-", "_")


@runtime_typing.checked
def _convert_key(
    object: Union[Dict[str, Any], Any], convert: Callable[[str], str]
) -> Union[Dict[str, Any], Any]:
    """Convert and update keys in a dictionary with "convert".

    Any value that is a dictionary will be recursively updated.
    Any value that is a list will be recursively searched.

    Args:
        object: The object to update.
        convert: The function to convert the keys, e.g. `kebab_case_to_snake_case`.

    Returns:
        The updated object.
    """
    if not isinstance(object, Dict):
        return object
    new_dict = {}
    for k, v in object.items():
        new_k = convert(k)
        if isinstance(v, Dict):
            new_v = _convert_key(v, convert)
        elif isinstance(v, List):
            new_v = [_convert_key(elem, convert) for elem in v]
        else:
            new_v = v
        if new_v is None:
            # Otherwise unnesseraily bloated sarif log with "null"s.
            continue
        if new_v == -1:
            # WAR: -1 as default value shouldn't be logged into sarif.
            continue

        new_dict[new_k] = new_v

    return new_dict


@runtime_typing.checked
def sarif_to_json(attr_cls_obj: _SarifClass, indent: Optional[str] = " ") -> str:
    dict = dataclasses.asdict(attr_cls_obj)
    dict = _convert_key(dict, snake_case_to_camel_case)
    return json.dumps(dict, indent=indent, separators=(",", ":"))


@runtime_typing.checked
def pretty_print_title(
    title: str, width: int = 80, fill_char: str = "=", print_output: bool = True
) -> str:
    """Pretty prints title in below format:

    ==================== title ====================
    """
    msg = f" {title} ".center(width, fill_char)
    if print_output:
        print(msg)
    return msg


@runtime_typing.checked
def pretty_print_item_title(
    title: str, fill_char: str = "=", print_output: bool = True
) -> str:
    """Pretty prints title in below format:

    title
    =====
    """
    msg_list = []
    msg_list.append(title)
    msg_list.append(fill_char * len(title))

    msg = "\n".join(msg_list)
    if print_output:
        print(msg)
    return msg


@runtime_typing.checked
def format_argument(obj: Any) -> str:
    return f"{type(obj)}"


@runtime_typing.checked
def display_name(fn: Callable) -> str:
    if hasattr(fn, "__qualname__"):
        return fn.__qualname__
    elif hasattr(fn, "__name__"):
        return fn.__name__
    else:
        return str(fn)

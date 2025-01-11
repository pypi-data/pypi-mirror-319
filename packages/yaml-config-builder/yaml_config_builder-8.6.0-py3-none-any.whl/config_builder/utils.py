# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Definition of utility methods that are used across the config-builder
"""

from __future__ import absolute_import, division, print_function

import logging
import os
from pathlib import Path, PurePath
from re import compile
from typing import Any, Dict, List

from config_builder.replacement_map import get_current_replacement_map

logger = logging.getLogger(__name__)


def replace_with_os_env(value: str) -> str:
    """
    Takes the given value and replaces all occurrences that match the
    given pattern ${...}, which corresponds to a specific os environment
    variable.

    Args:
        value: The value that should be checked for occurrences of os environment
               variables marked with ${...}

    Returns:
        The value with replaced occurrences of environment variables
    """
    # Pattern matches all occurrences of ${...} in the given value
    pattern = compile(r".*?\${(\w+)}.*?")
    matched_patterns = pattern.findall(value)

    for match in matched_patterns:
        os_value = os.environ.get(match)
        if os_value is not None:
            logger.debug(
                f"Replace os-environment '${{{match}}}' "
                f"in value '{value}' "
                f"with value '{os_value}'"
            )
            value = value.replace(f"${{{match}}}", os_value)

    return value


def replace_directory_in_path(
    file_path: str, replacement_key: str, replacement_value: str
) -> str:
    """
    Replaces directory in the given path.

    Args:
        file_path: String, a path to a file
        replacement_key: String, defining what is about to be replaced
        replacement_value: String, defining what the replacement looks like

    Returns: String, the updated file path

    """

    path_list = list(PurePath(file_path).parts)

    path_list = list(
        map(
            lambda x: x if x != replacement_key else replacement_value,
            path_list,
        )
    )
    return str(Path(os.sep.join(path_list)))


def prepare_config_path(config_path: str) -> str:
    """
    Take a config-path and an os-string-replacement-map and try to build a
    valid config-path by using the values of the os-string-replacement-map

    Args:
        config_path: input config-path

    Returns:
        the adapted config-path
    """

    string_replacement_map: Dict[str, str] = get_current_replacement_map()

    logger.debug(
        f"Given config-path does not exist: {config_path}. "
        f"These placeholder keys will be used for trying to build a "
        f"valid path: {string_replacement_map.keys()}"
    )

    for (
        key,
        value,
    ) in string_replacement_map.items():
        if value != "" and key in config_path:
            logger.debug(
                f"Replace '{key}' "
                f"in config-path '{config_path}' "
                f"with '{value}' "
            )

            config_path = replace_directory_in_path(
                file_path=config_path, replacement_key=key, replacement_value=value
            )

    config_path = replace_with_os_env(value=config_path)

    return str(Path(config_path))


def check_list_type(obj: List[Any], obj_type: Any) -> bool:
    """
    Check if the given list-object only contains objects of type 'obj_type'

    Args:
        obj: list that is to be checked
        obj_type: type that every object should match

    Returns:
        true if all items of the list are of type 'obj_type', false otherwise
    """
    return bool(obj) and all(isinstance(elem, obj_type) for elem in obj)

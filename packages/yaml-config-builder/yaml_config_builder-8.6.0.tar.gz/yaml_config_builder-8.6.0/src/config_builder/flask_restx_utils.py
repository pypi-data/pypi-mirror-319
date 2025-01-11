# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""Module for translating attr based configuration classes
to flaskx models. The models can be consumed in the flaskx
decorators to define the REST schema of the flaskx application.
"""

import inspect
import logging
from typing import Any, Dict, List, Optional, get_args

from attr import NOTHING
from attr import fields as attrs_fields

logger = logging.getLogger(__name__)


try:
    import flask_restx

    Namespace = flask_restx.Namespace
    Model = flask_restx.Namespace
    FlaskRestXList = flask_restx.fields.List
    FlaskRestXNested = flask_restx.fields.Nested
    FlaskRestXRaw = flask_restx.fields.Raw
    FlaskRestXInteger = flask_restx.fields.Integer
    FlaskRestXFloat = flask_restx.fields.Float
    FlaskRestXString = flask_restx.fields.String
    FlaskRestXBoolean = flask_restx.fields.Boolean
except ModuleNotFoundError as module_not_found_error:
    # pylint: disable=locally-disabled, multiple-statements, invalid-name
    logger.warning(
        "flask_restx is not installed. In order to use the features from"
        "config_builder.flask_restx_utils, install the config-builder with "
        "the extra 'flask-restx-utils'."
    )
    # Allow flask_restx to be optional
    flask_restx = None
    Namespace = None
    Model = None
    FlaskRestXList = None
    FlaskRestXNested = None
    FlaskRestXRaw = None
    FlaskRestXInteger = None
    FlaskRestXFloat = None
    FlaskRestXString = None
    FlaskRestXBoolean = None
    # pylint: enable=locally-disabled, multiple-statements, invalid-name


def create_docstring_info(attr_class: Any) -> Dict[str, Any]:
    """
    Create a dictionary with the docstring information of a configuration class.
    The docstring has to be in google format.

    REMARK: A ":" in the docstring text of an attribute, can lead to wrong docstring parsing

    Args:
        attr_class: The configuration class to extract the docstring information from

    Returns:
        A dictionary with the docstring information
    """

    doc_str: Optional[str] = inspect.getdoc(attr_class)

    if doc_str is None:
        return {}

    doc_split = [d.strip() for d in doc_str.split("\n") if d.strip() != ""]

    docstring_info = {}

    # Simply take every string that matches the pattern NAME:VALUE.
    # Later on, the docstring of an attribute is determined by matching
    # the attribute names with the key of this dictionary. Keys that
    # don't have a match will be ignored.
    current_attribute_name: Optional[str] = None
    for doc_line in doc_split:
        doc_line.strip()
        doc_line_split = doc_line.split(":")

        # All attributes in google format are stated as:  attribute_name: docstring
        if len(doc_line_split) == 2:
            current_attribute_name = doc_line_split[0].strip()
            docstring_info[current_attribute_name] = doc_line_split[1].strip()

        # If a new key has been found, except all following lines as docstring information.
        elif len(doc_line_split) == 1 and current_attribute_name in docstring_info:
            docstring_info[current_attribute_name] += f" {doc_line}"

    return docstring_info


def clean_module_name(attr_class: Any) -> str:
    """
    Get clean string representation of  class module name
    without the <class ...> part from the string representation
    of a class.

    Args:
        attr_class: The class for which to get the module name

    Returns:
        The clean module name of the class
    """
    name = str(attr_class)
    name = name.replace("'", "")
    name = name.replace('"', "")
    name = name.replace("<class", "")
    return name.replace(">", "").strip()


def resolve_field(
    api: Namespace,  # type: ignore[valid-type]
    field_name: str,
    field_type: Any,
    docstring_info: Dict[str, str],
    field_default: Optional[Any] = None,
) -> Optional[FlaskRestXRaw]:  # type: ignore[valid-type]
    """
    Resolve a single attribute field to a flask-restx field and
    add the respective model to the specified api.

    Args:
        api: The api to add the model to
        field_name: The name of the field to resolve
        field_type: The type of the field to resolve
        docstring_info: The docstring information dict from which to parse
                        the description for the flask-restx field
        field_default: The default for the flask-restx field

    Returns:
        The resolved flask-restx field or None if the field could not be resolved
    """

    if flask_restx is None:
        raise ValueError(
            "flask_restx is not installed. In order to use the feature, install "
            "the config-builder with the extra 'flask-restx-utils'"
        )

    field_doc: str = docstring_info.get(field_name, "")
    is_list: bool = False
    is_dict: bool = False

    if field_name.startswith("_"):
        return None

    required = True
    fields_args = get_args(field_type)
    # The first field arguments determine, whether an object is Optional or not.
    # This is the case when the type of the second argument is None.
    # If field is decorated with 'Optional' set required to False
    if len(fields_args) == 2 and fields_args[1] is type(None):
        required = False
        field_type = fields_args[0]

    # Per default all attributes of an attr class have the default-value NOTHING.
    # Check if the attribute has a default-value or not.
    if field_default is not None and field_default != NOTHING:
        required = False

    # The second time we scan the field arguments, we check if the field is a list.
    _fields_args = get_args(field_type)
    if str(List) in str(field_type) and len(_fields_args) == 1:
        field_type = _fields_args[0]
        is_list = True

    if str(Dict) in str(field_type):
        is_dict = True

    if not inspect.isclass(field_type):
        field_type = type(field_type)

    if is_list:
        resolved_field = resolve_field(
            api=api,
            field_name=field_name,
            field_type=field_type,
            docstring_info=create_docstring_info(attr_class=field_type),
        )

        if resolved_field is not None:
            return FlaskRestXList(
                required=required,
                description=field_doc,
                cls_or_instance=resolved_field,
            )

        return None

    if is_dict:
        return FlaskRestXNested(  # type: ignore[no-any-return]
            description=field_doc,
            required=required,
            model=api.model(  # type: ignore[attr-defined]
                name="DictionaryModel",
                model={},
            ),
        )

    if field_type is int:
        return FlaskRestXInteger(required=required, description=field_doc)  # type: ignore[no-any-return]

    if field_type is float:
        return FlaskRestXFloat(required=required, description=field_doc)  # type: ignore[no-any-return]

    if field_type is str:
        return FlaskRestXString(required=required, description=field_doc)  # type: ignore[no-any-return]

    if field_type is bool:
        return FlaskRestXBoolean(required=required, description=field_doc)  # type: ignore[no-any-return]

    model = recursive_resolve_fields(api=api, attr_class=field_type)

    if model is not None:
        return FlaskRestXNested(
            model=model,
            description=field_doc,
            required=required,
        )

    return None


def recursive_resolve_fields(api: Namespace, attr_class: Any) -> Optional[Model]:  # type: ignore[valid-type]
    """
    Recursively resolve fields of a config class to the respective flask_restx models.
    NOTE: By using this feature, the flaskx model attributes won't have a description.

    Args:
        api: The API were the created models are added to
        attr_class: The configuration class to resolve

    Returns:
        The resolved model or None if the model could not be resolved
    """
    field_dict: Dict[str, Any] = {}

    try:
        attr_class_fields = attrs_fields(attr_class)
    except Exception:
        return None

    docstring_info = create_docstring_info(attr_class=attr_class)

    for field in attr_class_fields:
        field_name: str = field.name

        created_field = resolve_field(
            api=api,
            field_name=field_name,
            field_type=field.type,
            field_default=field.default,
            docstring_info=docstring_info,
        )

        if created_field is not None:
            field_dict[field_name] = created_field

    module_name = clean_module_name(attr_class=attr_class)

    return api.model(  # type: ignore[attr-defined, no-any-return]
        name=module_name,
        model=field_dict,
        decription=f"A detailed description of the parameters can be found "
        f"in the documentation of the class '{module_name}",
    )

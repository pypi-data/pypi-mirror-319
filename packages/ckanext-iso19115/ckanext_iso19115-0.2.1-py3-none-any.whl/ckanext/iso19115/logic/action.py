from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

import ckan.plugins as p
import ckan.plugins.toolkit as tk

from xmlschema import etree_tostring
import ckanext.iso19115.utils as u
import ckanext.iso19115.converter as c
from ckanext.iso19115.interfaces import IIso19115

if TYPE_CHECKING:
    import ckanext.iso19115.types as t


def get_actions():
    return {
        "iso19115_package_show": package_show,
        "iso19115_package_check": package_check,
    }


@tk.side_effect_free
def package_check(context, data_dict):
    pkg = tk.get_action("iso19115_package_show")(context, data_dict)
    content = _pkg_into_xml(pkg)
    u.validate_schema(content, validate_codelists=True)
    u.validate_schematron(content)

    return True


@tk.side_effect_free
def package_show(context, data_dict):
    if data_dict.get("format") == "xml":
        pkg = tk.get_action("iso19115_package_show")(
            context, {"id": tk.get_or_bust(data_dict, "id")}
        )
        return _pkg_into_xml(pkg)

    pkg = tk.get_action("package_show")(context, data_dict)

    implementations = iter(p.PluginImplementations(IIso19115))
    conv: c.Converter = next(implementations).iso19115_metadata_converter(data_dict)
    conv.initialize(pkg)
    conv.process()
    conv.finalize()

    try:
        result = conv.build()
    except ValueError as e:
        raise tk.ValidationError({"schema": [str(e)]})

    return result


def _pkg_into_xml(pkg: dict[str, Any]):
    builder = u.get_builder("mdb:MD_Metadata")

    xml = builder.build(pkg)
    return bytes(etree_tostring(xml, namespaces=u.ns), "utf8")

# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any
import xmlschema
from ckanext.metaexport.formatters import Format
from ckanext.metaexport.formatters.pdf_format import PDFFormat
from ckanext.metaexport.formatters.html_format import HTMLFormat
from .utils import get_builder, ns


class Iso19115(Format):
    _content_type = "application/xml; charset=utf-8"

    def render(self, tpl, extra_vars):
        builder = get_builder("mdb:MD_Metadata")
        el: Any = builder.build(extra_vars)
        xml = xmlschema.etree_tostring(el, namespaces=ns)
        return xml


class Iso19115Html(HTMLFormat):
    pass


class Iso19115Pdf(PDFFormat):
    pass

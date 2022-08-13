# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# isort: skip_file

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath("."))  # To import config
sys.path.insert(0, os.path.abspath(".."))  # To import the main module

import docufix  # type: ignore

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_parser",
]

from config.basic import (
    author as author,
    copyright as copyright,
    exclude_patterns as exclude_patterns,
    html_static_path as html_static_path,
    html_theme as html_theme,
    language as language,
    project as project,
    release as release,
    templates_path as templates_path,
)

from config.autodoc import (
    autodoc_member_order as autodoc_member_order,
)

from config.napoleon import (
    napoleon_attr_annotations as napoleon_attr_annotations,
    napoleon_custom_sections as napoleon_custom_sections,
)

from config.i18n import (
    gettext_compact as gettext_compact,
    locale_dirs as locale_dirs,
)

from config.myst import (
    source_suffix as source_suffix,
)

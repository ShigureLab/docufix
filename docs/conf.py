# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath("."))  # To import config
sys.path.insert(0, os.path.abspath(".."))  # To import the main module

import docufix  # type: ignore

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

from config.autodoc import (
    autodoc_member_order as autodoc_member_order,
)

from config.napoleon import (
    napoleon_custom_sections as napoleon_custom_sections,
    napoleon_attr_annotations as napoleon_attr_annotations,
)

from config.i18n import (
    locale_dirs as locale_dirs,
    gettext_compact as gettext_compact,
)

from config.basic import (
    project as project,
    copyright as copyright,
    author as author,
    release as release,
    templates_path as templates_path,
    language as language,
    exclude_patterns as exclude_patterns,
    html_theme as html_theme,
    html_static_path as html_static_path,
)

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

from config.autodoc import autodoc_member_order as autodoc_member_order
from config.basic import author as author
from config.basic import copyright as copyright
from config.basic import exclude_patterns as exclude_patterns
from config.basic import html_static_path as html_static_path
from config.basic import html_theme as html_theme
from config.basic import language as language
from config.basic import project as project
from config.basic import release as release
from config.basic import templates_path as templates_path
from config.i18n import gettext_compact as gettext_compact
from config.i18n import locale_dirs as locale_dirs
from config.napoleon import napoleon_attr_annotations as napoleon_attr_annotations
from config.napoleon import napoleon_custom_sections as napoleon_custom_sections

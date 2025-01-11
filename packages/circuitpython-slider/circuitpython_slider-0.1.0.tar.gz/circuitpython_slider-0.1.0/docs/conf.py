# SPDX-FileCopyrightText: 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import os
import sys
import datetime

sys.path.insert(0, os.path.abspath(".."))

# -- General configuration ------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "CircuitPython": ("https://docs.circuitpython.org/en/latest/", None),
}

autodoc_mock_imports = [
    "digitalio",
    "vectorio",
    "adafruit_display_shapes",
    "bitmaptools",
    "busio",
    "adafruit_touchscreen",
    "adafruit_display_text",
    "displayio",
    "adafruit_displayio_layout",
]

autoclass_content = "both"
# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
# General information about the project.
project = " CircuitPython slider Library"
copyright = "2021 Jose David M."
author = "Jose David M."

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = "1.0"
# The full version, including alpha/beta/rc tags.
release = "1.0"

language = "en"
autoclass_content = "both"
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".env",
    "CODE_OF_CONDUCT.md",
]

default_role = "any"
add_function_parentheses = True
pygments_style = "sphinx"
todo_include_todos = False
todo_emit_warnings = False
napoleon_numpy_docstring = False

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
on_rtd = os.environ.get("READTHEDOCS", None) == "True"

if not on_rtd:  # only import and set the theme if we're building docs locally
    try:
        import sphinx_rtd_theme

        html_theme = "sphinx_rtd_theme"
        html_theme_path = [sphinx_rtd_theme.get_html_theme_path(), "."]
    except:
        html_theme = "default"
        html_theme_path = ["."]
else:
    html_theme_path = ["."]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#
html_favicon = "_static/favicon.ico"

# Output file base name for HTML help builder.
htmlhelp_basename = "CircuitPython_SliderLibrarydoc"

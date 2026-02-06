from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pybtex.plugin import register_plugin
from pybtex.richtext import Text
from pybtex_docutils import Backend

from sphinx_pybtex_etal_style._support_bibtex_math import (
    patch_format_math,
    patch_from_latex,
)
from sphinx_pybtex_etal_style.style import UnsrtEtAl

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment


def setup(app: Sphinx) -> dict[str, Any]:
    app.add_config_value(
        "unsrt_etal_isbn_resolver", default="bookfinder", rebuild="env"
    )
    app.add_config_value("bibtex_use_mathjax", default=False, rebuild="env")
    app.connect("config-inited", register_style)
    app.connect("config-inited", register_math_support)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


def register_style(app: Sphinx, __: BuildEnvironment) -> None:
    UnsrtEtAl.isbn_resolver = app.config.unsrt_etal_isbn_resolver
    register_plugin("pybtex.style.formatting", "unsrt_et_al", UnsrtEtAl)


def register_math_support(app: Sphinx, __: BuildEnvironment) -> None:
    if not app.config.bibtex_use_mathjax:
        return
    Text.from_latex = patch_from_latex  # ty:ignore[invalid-assignment]
    if Backend.default_suffix != ".txt":
        Backend.format_math = patch_format_math  # ty:ignore[unresolved-attribute]

# pyright: reportMissingTypeStubs=false
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pybtex.plugin import register_plugin

from sphinx_pybtex_etal_style.style import UnsrtEtAl

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment


def setup(app: Sphinx) -> dict[str, Any]:
    app.add_config_value(
        "unsrt_etal_isbn_resolver", default="bookfinder", rebuild="env"
    )
    app.connect("config-inited", register_style)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


def register_style(app: Sphinx, __: BuildEnvironment) -> None:
    UnsrtEtAl.isbn_resolver = app.config.unsrt_etal_isbn_resolver
    register_plugin("pybtex.style.formatting", "unsrt_et_al", UnsrtEtAl)

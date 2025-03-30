import pytest
from pathlib import Path
from typing import Callable

from docutils.core import publish_doctree
from sphinx.testing.util import SphinxTestApp

SRC_DIR = Path(__file__).parent.parent


@pytest.fixture
def sphinx_app(tmp_path: Path, make_app) -> Callable:
    docs_source_dir = tmp_path / "source"
    docs_source_dir.mkdir()
    docs_build_dir = tmp_path / "build"
    docs_build_dir.mkdir()

    conf_kwargs = {
        "extensions": ["autodoc_directory_structure"],
    }
    conf_content = "\n".join(
        [f"{key} = {value!r}" for key, value in conf_kwargs.items()]
    )

    conf_py = (docs_source_dir / "conf.py").write_text(conf_content)

    app = make_app(
        srcdir=docs_source_dir,
        builddir=docs_build_dir,
        buildername="html",
    )

    return app


def test_directive_dogfood_html(sphinx_app: SphinxTestApp):
    index_rst = sphinx_app.srcdir / "index.rst"
    index_rst.write_text(f"""
    .. autodoc_directory_structure:: {SRC_DIR}
        :gitignore:
    """)

    index_html = sphinx_app.outdir / "index.html"

    sphinx_app.build()
    index_html_contains = (
        '<li><p><code class="docutils literal notranslate"><span class="pre">'
        'autodoc_directory_structure/'
        '</span></code> - The top-level package directory.</p>'
    )

    assert index_html_contains in index_html.read_text()

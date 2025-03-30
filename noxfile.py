from __future__ import annotations

from pathlib import Path

import nox

DIR = Path(__file__).parent.resolve()

nox.needs_version = ">=2024.3.2"
nox.options.sessions = ["test"]
nox.options.default_venv_backend = "uv|virtualenv"


@nox.session
def test(session: nox.Session) -> None:
    """Run the unit tests."""
    session.install(".")

    pyproject = nox.project.load_toml("pyproject.toml")
    session.install(*nox.project.dependency_groups(pyproject, "test"))

    session.run("pytest", *session.posargs)

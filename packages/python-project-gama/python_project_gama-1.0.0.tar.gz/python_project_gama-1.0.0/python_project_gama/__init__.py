# type: ignore[attr-defined]
"""Awesome `python-project-gama` is a Python cli/package created with https://gitlab.com/manoelpqueiroz/galactipy."""

from importlib import metadata

from python_project_gama.example import hello


def _get_version() -> str:
    try:
        return metadata.version("python-project-gama")
    except ModuleNotFoundError:  # pragma: no cover
        return "unknown"


__version__ = _get_version()

__all__ = ['hello']

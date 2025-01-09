# type: ignore[attr-defined]
"""Awesome `python-project-beta` is a Python cli/package created with https://gitlab.com/manoelpqueiroz/galactipy."""

from importlib import metadata

from python_project_beta.example import hello


def _get_version() -> str:
    try:
        return metadata.version("python-project-beta")
    except ModuleNotFoundError:  # pragma: no cover
        return "unknown"


__version__ = _get_version()

__all__ = ['hello']

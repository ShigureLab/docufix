# Meta information for the project.
from __future__ import annotations

__version__ = "0.3.2"
__author__ = "Nyakku Shigure"
__year__ = "2022"
__project_info__ = {
    "name": __name__,
    "version": __version__,
    "copyright": f"{__year__}, {__author__}",
    "author": __author__,
}

# The exported modules.
from .core import File, Line, Rule

__all__ = [
    "Line",
    "File",
    "Rule",
]

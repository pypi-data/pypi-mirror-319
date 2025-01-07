"""Init."""

import importlib.metadata

from . import logger


__version__ = importlib.metadata.version(__name__)



__all__ = [
    "__version__",
    "logger",
]


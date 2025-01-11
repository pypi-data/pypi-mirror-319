"""Flukit: A toolkit for influenza sequence analysis.

This package provides tools for manipulating influenza sequences,
including reference numbering and introducing mutations based on reference sequence numbering.
"""

from .utils import NumberedResidue, NumberedProtein
from .align import ref_numbering
from .refseq import H3ref, H1ref, H5ref
import logging


def log(level=logging.DEBUG):
    """Configure logging for the flukit package.

    Args:
        level: The logging level to set. Defaults to logging.DEBUG.

    Returns:
        None

    Example:
        >>> import flukit
        >>> flukit.log()  # Sets up logging with DEBUG level
    """
    logger = logging.getLogger(__package__)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return None


__all__ = [
    "NumberedResidue",
    "NumberedProtein",
    "ref_numbering",
    "H3ref",
    "H1ref",
    "H5ref",
]

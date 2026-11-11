"""astrolab: agent-driven, laptop-scale astronomy research environment.

Core principle: MB-scale local data, minute-scale compute. Push heavy lifting to
public servers (ADQL/TAP) and compressed data products. See design/000-*.md.
"""
from . import config
from .fetch import TooLarge

__all__ = ["config", "TooLarge"]
__version__ = "0.1.0"

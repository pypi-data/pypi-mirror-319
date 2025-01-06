"""
IIIF Downloader
==============

A Python package to download images from IIIF manifests.
"""

from .image import IIIFImage
from .manifest import IIIFManifest
from .config import Config, config

__version__ = "0.1.6"

__all__ = ["IIIFManifest", "IIIFImage", "config", "Config"]

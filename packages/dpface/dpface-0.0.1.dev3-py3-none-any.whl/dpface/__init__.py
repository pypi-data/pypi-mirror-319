import logging, os, sys

logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])
logger.debug(__file__)
# coding: utf-8
# pylint: disable=wrong-import-position
"""DPFace: A Face Analysis Toolkit."""
try:
    import onnxruntime
except ImportError:
    raise ImportError("Unable to import dependency onnxruntime. ")

__version__ = "0.0.1.dev3"

from . import model_zoo
from . import utils
from . import app


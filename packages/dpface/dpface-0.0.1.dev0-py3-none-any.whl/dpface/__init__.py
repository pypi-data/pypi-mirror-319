# coding: utf-8
# pylint: disable=wrong-import-position
"""DPFace: A Face Analysis Toolkit."""
from __future__ import absolute_import

try:
    import onnxruntime
except ImportError:
    raise ImportError(
        "Unable to import dependency onnxruntime. "
    )

__version__ = '0.0.1.dev0'

from . import model_zoo
from . import utils
from . import app
from . import data
from . import thirdparty


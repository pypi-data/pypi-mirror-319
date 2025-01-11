import logging, os, sys

logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])
logger.debug(__file__)
from .face_analysis import *

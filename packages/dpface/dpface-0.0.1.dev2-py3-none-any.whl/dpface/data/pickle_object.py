import logging, os, sys

logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])
logger.debug(__file__)
import os.path as osp
from pathlib import Path
import pickle


def get_object(name):
    objects_dir = osp.join(Path(__file__).parent.absolute(), "objects")
    if not name.endswith(".pkl"):
        name = name + ".pkl"
    filepath = osp.join(objects_dir, name)
    if not osp.exists(filepath):
        return None
    with open(filepath, "rb") as f:
        obj = pickle.load(f)
    return obj

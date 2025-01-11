import logging, os, sys

logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])
logger.debug(__file__)
from abc import ABC, abstractmethod
from argparse import ArgumentParser


class BaseDPFaceCLICommand(ABC):
    @staticmethod
    @abstractmethod
    def register_subcommand(parser: ArgumentParser):
        raise NotImplementedError()

    @abstractmethod
    def run(self):
        raise NotImplementedError()

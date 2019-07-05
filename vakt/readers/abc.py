"""
Contains interfaces that all Readers should implement.
"""

from abc import ABCMeta, abstractmethod


class Reader(metaclass=ABCMeta):
    @abstractmethod
    def read(self, file):
        pass

    @abstractmethod
    def populate(self, file, storage):
        pass
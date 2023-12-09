from abc import ABC, abstractclassmethod

class mapper(ABC):
    @abstractclassmethod
    def run(self):
        pass
from abc import ABC, abstractmethod

class mapper(ABC):
    
    def __init__(self, db, yaml_row, log):
        self.db = db
        self.yaml_row = yaml_row
        self.log = log

    
    @abstractmethod
    def check(self):
        pass
    
    
    @abstractmethod
    def run(self):
        pass
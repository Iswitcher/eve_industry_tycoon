from abc import ABC, abstractmethod

class mapper(ABC):
    
    def __init__(self, db_path, yaml, log):
        self.db = db_path
        self.yaml = yaml
        self.log = log
        
    
    @abstractmethod
    def run(self):
        pass
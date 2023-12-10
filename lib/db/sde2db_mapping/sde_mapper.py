from abc import ABC, abstractmethod

class mapper(ABC):
    
    def __init__(self, db_path, yaml):
        self.db = db_path
        self.yaml = yaml
        
    
    @abstractmethod
    def run(self):
        pass
import logging

class logger:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    
    def info(self, text):
        self.logger.info(text)
    
        
    def warning(self, text):
        self.logger.warning(text)
    
        
    def critical(self, text):
        self.logger.critical(text)
import logging

class log:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    def info(text):
        log.logger.info(text)
        
    def warning(text):
        log.logger.warning(text)
        
    def critical(text):
        log.logger.critical(text)
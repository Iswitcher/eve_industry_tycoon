import logging
from logging import handlers
import os

class logger:
    def __init__(self, log_to_file:bool=False):
        self.logger = logging.getLogger(__name__)
        level = logging.INFO
        self.logger.setLevel(level)

        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        if log_to_file:
            filename = self.getLogFilename()
            # TODO: Move backupCount to the config
            handler = handlers.RotatingFileHandler(filename=filename,
                                                   backupCount=10)
            handler.doRollover()
            handler.setLevel(level)
            self.logger.addHandler(handler)


    def getLogFilename(self)->str:
        # TODO: Move the logs path/name to the config
        logs_dir = os.getcwd() + "/logs"
        if not os.path.isdir(logs_dir):
            os.makedirs(logs_dir)
        # TODO: Move this constant to the config
        return os.path.join(logs_dir, "log.txt")


    def info(self, text):
        self.logger.info(text)


    def warning(self, text):
        self.logger.warning(text)


    def critical(self, text):
        self.logger.critical(text)

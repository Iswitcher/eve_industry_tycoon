import os
import json
import traceback

from lib.logger import logger
from collections import namedtuple

def customJsonDecoder(json):
    return namedtuple('X', json.keys())(*json.values())

class cfg_reader:
    
    # fetch and return config json
    def get_config_json(self, path):
        try:
            file = open(path)
            data = json.load(file, object_hook=customJsonDecoder)
            return data
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            logger.critical(f'ERROR in {method_name}: {e}')
            return {}
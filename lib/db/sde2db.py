import yaml
import importlib
import re
import traceback

from lib.cfg_reader import cfg_reader
from lib.db.db_utils import db_utils
from lib.logger import logger


class sde2db:
    
    def __init__(self):
        self.log = logger(None)
        self.db_path = 'resources/sde.db'
        self.db = db_utils(self.db_path, None)
        self.cfg = cfg_reader()
        self.cfg_file = 'config/sde_import.json'
        self.sde_mapping_path = 'lib.db.sde2db_mapping.fsd.' #TODO: a better solution mb?
    
    
    # main conversion method
    def sde_convert_all(self):
        try:
            cfg_file = self.cfg.get_config_json(self.cfg_file)
            yamls = cfg_file.yaml_to_convert
            for path in yamls:
                self.sde_convert_yaml(path)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    # retrieve abstract class by name
    def sde_abs_class_import(self, path):
        try:
            re_pattern = re.compile(r'\w+(?=.yaml)')
            module_name = re.search(re_pattern, path).group()
            module = importlib.import_module(self.sde_mapping_path + module_name)
            cls = getattr(module, module_name)
            return cls
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # read yaml file
    def sde_yaml_read(self, path):
        try:
            with open(path, 'r', encoding="utf-8") as yaml_file:
                yaml_data = yaml.safe_load(yaml_file)
                return yaml_data
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
   # get the reference conversion class and run the yaml2sql conversion
    def sde_convert_yaml(self, path):
        try:
            self.log.info(f'Converting the {path}')
            yaml_file = self.sde_yaml_read(path)
            module = self.sde_abs_class_import(path)
            module_instance = module(self.db_path, yaml_file)
            module_instance.run()
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
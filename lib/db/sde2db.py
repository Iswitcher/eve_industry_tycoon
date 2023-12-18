import yaml
import importlib
import re
import traceback
import time

from lib.cfg_reader import cfg_reader
from lib.db.db_utils import db_utils

class sde2db:
    
    def __init__(self, log):
        self.log = log
        self.db_path = 'resources/sde.db'
        self.db = db_utils(self.log, self.db_path, None, None)
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
            module_path = self.sde_mapping_path + module_name
            module = importlib.import_module(module_path)
            cls = getattr(module, module_name)
            return cls
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # read yaml file
    def sde_yaml_read(self, path):
        try:
            with open(path, 'r', encoding="utf-8") as yaml_file:
                # yaml_data = yaml.safe_load(yaml_file)
                yaml_data = yaml.load(yaml_file, Loader=yaml.CBaseLoader)
                return yaml_data
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
   # get the reference conversion class and run the yaml2sql conversion
    def sde_convert_yaml(self, path):
        try:
            t_start = time.time()
            self.log.info(f'Start converting: {path}')
            yaml_file = self.sde_yaml_read(path)
            t = round(time.time() - t_start, 4)
            self.log.info(f'yaml: {path} is read, {t}s passed.')
            
            module = self.sde_abs_class_import(path)
            module_instance = module(self.db, self.log)
            
            self.db.db_check()
            self.db.db_connect()
            
            module_instance.check()
            module_instance.start()
            for row in yaml_file:
                module_instance.run(row, yaml_file[row])
            module_instance.finish()
            
            self.db.db_commit()
            self.db.db_disconnect()
            t = round(time.time() - t_start, 4)
            self.log.info(f'Finish converting: {path}, {t}s passed.')
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')

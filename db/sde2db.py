import yaml

from db.db_utils import db_utils

class sde2db:
    
    def __init__(self, checksum):
        self.checksum = checksum
        self.sde_db_path = 'sde.db'
        
        self.sde_categories = 'sde/fsd/categoryIDs.yaml' 
    
    
    # main conversion method
    def sde_convert_all(self):
        self.sde_covert_categoryids()
        
        
    # convert categoryIDs.yaml to DB
    def sde_covert_categoryids(self):    
        with open(self.sde_categories, 'r', encoding="utf-8") as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
            
        db = db_utils(self.sde_db_path, None)
        conn = db.db_connect()
        blah = 123
        # TODO import logic
            
    
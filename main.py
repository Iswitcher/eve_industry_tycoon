import json
import zipfile
import os
import shutil
import glob
import yaml
import re
import traceback

from db import db
from web import web
from log import log

from collections import namedtuple

'''
TODO:
 - sqlite db CRUD
 - load sde
 - load icons
'''

def customJsonDecoder(json):
        return namedtuple('X', json.keys())(*json.values())

class Main:
    file_endpoints  = 'esi_endpoints'
    file_checksum   = 'sde_checksum'
    file_config     = 'config'

    endpoints = {}
    config = {}
    
    # load config file
    def load_config(self):
        log.info(f'Config loading')
        try: 
            file = open(self.file_config)
            self.config = json.load(file, object_hook=customJsonDecoder)
            log.info(f'Config loaded')
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')
    
    
    # load URL endpoints file
    def load_endpoints(self):
        log.info('ESI endpoints loading')
        try: 
            file = open(self.file_endpoints)
            self.endpoints = json.load(file)
            log.info('ESI endpoints loaded')
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')
    
    
    # get the old sde checksum
    def load_old_checksum(self):
        log.info('Loading old SDE checksum')
        try:   
            file = open(self.file_checksum)
            self.checksum = file.read()
            log.info(f'SDE old checksum is: {self.checksum}')
            file.close()
            return self.checksum
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')
            return ''            

    
    # get the new sde checksum
    def load_new_checksum(self):
        try:
            # log.info('Fetching SDE checksum')
            checksum_url = self.endpoints['sde_checksum_url']
            checksum = web.get_sde_checksum(checksum_url)
            log.info(f'SDE new checksum is: {checksum}')
            return checksum
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')
        
            
    # is checksum changed?   
    def validate_sde_hash(self):
        try:        
            old_checksum = self.load_old_checksum()
            new_checksum = self.load_new_checksum()
        
            if old_checksum != new_checksum:
                log.warning(f'SDE checksum NOT equal')
                self.update_checksum(new_checksum)
                self.download_sde_zip()
            elif os.path.exists(self.config.sde_path) == False:
                log.warning(f'SDE folder not found! Double checking.')
                self.download_sde_zip()
            else: 
                log.info(f'SDE checksum matched')  
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')      
       
            
    # save new sde checksum
    def update_checksum(self, new_checksum):
        try:
            file = open(self.file_checksum, "w")
            file.write(new_checksum)
            log.info(f'Checksum updated: {new_checksum}')
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')
  

    # download sde zip
    def download_sde_zip(self):
        try:
            url = self.endpoints['sde_download_url']
            zip = web.get_sde_zip(url)
            self.clean_sde(self.config.sde_path)
            self.extract_zip(zip)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')   
    
    
    # clean old SDE folder if needed
    def clean_sde(self, folder):
        try:
            if os.path.exists(folder):
                log.info(f'Clearing old SDE records')
                shutil.rmtree(folder)
                return
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')  
        
    
    # exctract zip to app folder    
    def extract_zip(self, data):
        try:
            log.info('Extracting zip')
            with zipfile.ZipFile(data, 'r') as zip:
                zip.extractall('')
                log.info('ZIP Extracted successfully')
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')
            
            
    # take yaml and paste its data into sql    
    def sde_convert(self):
        try:
            sde_db_path = self.config.sde_db_path
            file_list = self.filter_yaml_file_list()
            for yaml in file_list:
                log.info(f'Processing file {1+file_list.index(yaml)} from {len(file_list)}')
                log.info(f'Extracting {yaml}')
                data = self.get_yaml_data(yaml)
                table = self.get_table_name(yaml)                
                conn = db.connect(sde_db_path)
                db.yaml_to_sql(conn, table, data)
                db.disconnect(conn)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')   
    
    
    # get table name from yaml
    def get_table_name(self, filepath):
        try:
            regex = '\w+(?=.yaml)'
            table = re.search(regex, filepath).group()
            return table
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')                


    # match downloaded files vs config
    def filter_yaml_file_list(self):
        output = []
        all_files = glob.glob(self.config.sde_path + '/**/*.yaml', recursive=True)
        for file in all_files:
            for to_sql in self.config.sde_to_sql_files:
                if file.endswith(to_sql):
                    output.append(file)
                    log.info(f'Adding {to_sql} to parse queue')
        return output    
    
    
    # get yaml data from file
    def get_yaml_data(self, path):
        try:
            with open(path, 'r', encoding='utf8') as file:
                yaml_object = yaml.safe_load(file)
                return yaml_object
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')       


    # main execution
    def run(self):
        # load config
        self.load_config()
        
        # load endpoints
        self.load_endpoints()
        
        # check SDE hash 
        self.validate_sde_hash()  

        # parse SDE dump into SQLite
        self.sde_convert()
           
            
if __name__ == '__main__':
    Main().run()
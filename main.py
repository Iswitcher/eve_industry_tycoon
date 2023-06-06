import json
import requests
import zipfile
import io
import os
import glob
import yaml
import re

from web import web
from db import db
from log import log

from collections import namedtuple
from json import JSONEncoder

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
            log.critical(f'Error while loading main config: {e}')
    
    
    # load URL endpoints file
    def load_endpoints(self):
        log.info('ESI endpoints loading')
        try: 
            file = open(self.file_endpoints)
            self.endpoints = json.load(file)
            log.info('ESI endpoints loaded')
        except Exception as e:
            log.critical(f'Error while loading ESI endpoints: {e}')
    
    
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
            log.critical(f'SDE checksum NOT found/loaded: {e}')
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
            log.critical(f'Failed to get new SDE checksum: {e}')
        
            
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
            log.critical(f'Failed to match checksum: {e}')      
       
            
    # save new sde checksum
    def update_checksum(self, new_checksum):
        try:
            file = open(self.file_checksum, "w")
            file.write(new_checksum)
            log.info(f'Checksum updated: {new_checksum}')
        except Exception as e:
            log.critical(f'Failed to write new SDE checksum: {e}')
  

    # download sde zip
    def download_sde_zip(self):
        try:
            url = self.endpoints['sde_download_url']
            log.info('Fetching zip')
            response = requests.get(url, stream=True)
            
            if response.status_code == 200:
                zip = io.BytesIO(response.content)
                self.clean_sde(self.config.sde_path)
                self.extract_zip(zip)
            else:
                log.critical(f'Failed to download zip: HTTP {response.status_code}')
        except Exception as e:
            log.critical(f'Failed to write new SDE checksum: {e}')    
    
    
    # clean old SDE folder if needed
    def clean_sde(self, folder):
        try:
            if os.path.exists(folder):
                log.info(f'Clearing old SDE records')
                os.remove(folder)
                return
        except Exception as e:
            log.critical(f'Failed to purge old SDE folder: {e}')  
        
    
    # exctract zip to app folder    
    def extract_zip(self, data):
        try:
            log.info('Extracting zip')
            with zipfile.ZipFile(data, 'r') as zip:
                zip.extractall('')
                log.info('ZIP Extracted successfully')
        except Exception as e:
            log.critical(f'Error while extracting: {e}')

    
    # take yaml and paste its data into sql    
    def sde_convert(self):
        sde_db_path = self.config.sde_db_path
        conn = db.connect(sde_db_path)
        
        file_list = self.filter_yaml_file_list()
        for path in file_list:
            log.info(f'Extracting {path}')
            table = self.yaml_get_table_name(path)
            filedata = self.get_yaml_data(path)
            self.yaml_2_sql(table, filedata)
        db.disconnect(conn)
        log.info(f'DB Connection closed')
                    

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

    
    # get sql table name from filename    
    def yaml_get_table_name(self, path):
        regex = '\w+(?=.yaml)'
        return re.search(regex, path).group()
    
    
    # get yaml data from file
    def get_yaml_data(self, path):
        try:
            with open(path, 'r') as file:
                yaml_object = yaml.safe_load(file)
                return file
        except Exception as e:
            log.critical(f'Failed to get yaml data (file {path}): {e}') 
     
    
    # Extract yaml into sql table
    def yaml_2_sql(self, table, data):
        log.critical('DUMMY')
    #     with open('your_file.yaml', 'r') as file:
    # # Load the YAML contents into a Python object
    # yaml_object = yaml.safe_load(file)
    
        

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
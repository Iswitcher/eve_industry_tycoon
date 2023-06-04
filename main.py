import datetime
import json
import sqlite3
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


    # get current time
    def time(self):
        time = datetime.datetime.now()
        time = time.strftime('%Y-%m-%d %H:%M:%S')
        return time
    

    # compose log message
    def log(self, message, status=''):
        if status == 'w':
            p_status = '[WARNING]'
        elif status == 'e':
            p_status = '[ERROR]'
        else: p_status = ''
        print(f'[{self.time()}]{p_status} {message}')
    
    
    # load config file
    def load_config(self):
        self.log(f'Config loading')
        try: 
            file = open(self.file_config)
            self.config = json.load(file, object_hook=customJsonDecoder)
            self.log(f'Config loaded')
        except Exception as e:
            self.log(f'Error while loading main config: {e}', 'e')
    
    
    # load URL endpoints file
    def load_endpoints(self):
        self.log('ESI endpoints loading')
        try: 
            file = open(self.file_endpoints)
            self.endpoints = json.load(file)
            self.log('ESI endpoints loaded')
        except Exception as e:
            self.log(f'Error while loading ESI endpoints: {e}', 'e')
    
    
    # get the old sde checksum
    def load_old_checksum(self):
        self.log('Loading old SDE checksum')
        try:
            file = open(self.file_checksum)
            self.checksum = file.read()
            self.log(f'SDE old checksum is: {self.checksum}')
            return self.checksum
        except Exception as e:
            self.log(f'SDE checksum NOT found/loaded: {e}', 'w')
            return ''            
    
    
    # get the new sde checksum
    def load_new_checksum(self):
        try:
            sde_checksum_url = self.endpoints['sde_checksum_url']
            self.log(f'Fetching SDE checksum at: {sde_checksum_url}')
            response = requests.get(sde_checksum_url, allow_redirects=True)
            if response.status_code == 200:
                self.log(f'SDE new checksum is: {response.text}')
                return response.text
            else:
                self.log(f'HTTP response code not 200: {response.status_code}', 'w')
                return ''
        except Exception as e:
            self.log(f'Failed to get new SDE checksum: {e}')
        
            
    # is checksum changed?   
    def validate_sde_hash(self):        
        old_checksum = self.load_old_checksum()
        new_checksum = self.load_new_checksum()
        
        if old_checksum != new_checksum:
            self.log(f'SDE checksum NOT equal', 'w')
            self.update_checksum(new_checksum)
            self.download_sde_zip()
        elif os.path.exists(self.config.sde_path) == False:
            self.log(f'SDE folder not found! Double checking.')
            self.download_sde_zip()
        else: 
            self.log(f'SDE checksum matched')    
       
            
    # save new sde checksum
    def update_checksum(self, new_checksum):
        try:
            file = open(self.file_checksum, "w")
            file.write(new_checksum)
            self.log(f'Checksum updated: {new_checksum}')
        except Exception as e:
            self.log(f'Failed to write new SDE checksum: {e}')
  

    # download sde zip
    def download_sde_zip(self):
        url = self.endpoints['sde_download_url']
        self.log('Fetching zip')
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            zip = io.BytesIO(response.content)
            if os.path.exists(self.config.sde_path):
                self.log(f'Clearing old SDE records')
                os.remove(self.config.sde_path)
            self.extract_zip(zip)
        else:
            self.log(f'Failed to download zip: HTTP {response.status_code}', 'e')
        
    
    # exctract zip to app folder    
    def extract_zip(self, data):
        try:
            self.log('Extracting zip')
            with zipfile.ZipFile(data, 'r') as zip:
                zip.extractall('')
                self.log('ZIP Extracted successfully')
        except Exception as e:
            self.log(f'Error while extracting: {e}', 'e')

    
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
        db.disconnect(sde_db_path)
                    

    # match downloaded files vs config
    def filter_yaml_file_list(self):
        output = []
        all_files = glob.glob(self.config.sde_path + '/**/*.yaml', recursive=True)
        for file in all_files:
            for to_sql in self.config.sde_to_sql_files:
                if file.endswith(to_sql):
                    output.append(file)
                    self.log(f'Adding {to_sql} to parse queue')
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
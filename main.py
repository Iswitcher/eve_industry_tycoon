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
    def parse_sde_into_sql(self):
        self.check_db_file()
        files = self.get_file_list()
        for file in files:
            self.log(f'Extracting {file}')
            self.extract_yaml(file)
                    
    
    # create db file if not exists
    def check_db_file(self):
        if not os.path.exists(self.config.sde_db_path):
            self.log(f'No DB file found! Creating a new one')
            conn = sqlite3.connect(self.config.sde_db_path)
            conn.commit()
            conn.close
        else: 
            self.log(f'DB file found')  
    
    
    # match downloaded files vs config
    def get_file_list(self):
        output = []
        all_files = glob.glob(self.config.sde_path + '/**/*.yaml', recursive=True)
        for file in all_files:
            for to_sql in self.config.sde_to_sql_files:
                if file.endswith(to_sql):
                    output.append(file)
                    self.log(f'Adding {to_sql} to parse queue')
        return output
    
    
    # extract yaml into sql table
    def extract_yaml(self, file):
        try:
            table = self.yaml_get_table_name(file)
            self.check_or_create_sql_table(table)
        except Exception as e:
            self.log(f'Error while extracting yaml: {e}', 'e')   
             
       
    # get sql table name from filename    
    def yaml_get_table_name(self, path):
        regex = '\w+(?=.yaml)'
        return re.search(regex, path).group()
    
    
    # create sql table if not exsists
    def check_or_create_sql_table(self, table):
        try:
            conn = sqlite3.connect(self.config.sde_db_path)
            if self.table_exists(table, conn):
                self.log(f'The table {table} exists.')
            else:
                self.log(f'The table {table} does not exist. Creating.')
                self.sql_create_new_table(conn, table)
            conn.close
        except Exception as e:
            self.log(f'Error while checking db table: {e}', 'e') 
    
    
    # check if sql table exists
    def table_exists(self, table, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
        return cursor.fetchone() is not None
    
    
    # create table with standard fields 
    def sql_create_new_table(self, conn, table):
        cursor = conn.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table} (
                    uid INTEGER PRIMARY KEY,
                    start_date DATE,
                    end_date DATE
                )''')
        self.log(f'Table {table} created!')       
        

    # main execution
    def run(self):
        # load config
        self.load_config()
        
        # load endpoints
        self.load_endpoints()
        
        # check SDE hash 
        self.validate_sde_hash()  

        # parse SDE dump into SQLite
        self.parse_sde_into_sql()
           
            
if __name__ == '__main__':
    Main().run()
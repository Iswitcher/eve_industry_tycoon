import datetime
import json
import sqlite3
import requests
import zipfile
import io
import os
# import sqlite3

'''
TODO:
 - sqlite db CRUD
 - load sde
 - load icons
'''

class Main:
    file_endpoints  = 'esi_endpoints'
    file_checksum   = 'sde_checksum'

    endpoints = {}
    
    sde_path = 'sde'
    sde_db_path = 'sde.db'
    

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
      
    
    # load URL endpoints file
    def load_endpoints(self):
        self.log('ESI endpoints config loading')
        try: 
            file = open(self.file_endpoints)
            self.endpoints = json.load(file)
            self.log('ESI endpoints config loaded')
        except Exception as e:
            self.log(f'Error while loading ESI endpoints config: {e}', 'e')
    
    
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
        elif os.path.exists(self.sde_path) == False:
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
            if os.path.exists(self.sde_path):
                self.log(f'Clearing old SDE records')
                os.remove(self.sde_path)
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


    
    def parse_sde_into_sql(self):
        if not os.path.exists(self.sde_db_path):
            conn = sqlite3.connect(self.sde_db_path)
            conn.commit()
            conn.close

    def run(self):
        # load endpoints
        self.load_endpoints()
        
        # check SDE hash 
        self.validate_sde_hash()  

        # parse SDE dump into SQLite
        self.parse_sde_into_sql()
            
            
if __name__ == '__main__':
    Main().run()
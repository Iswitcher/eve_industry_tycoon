import json
import requests
import sqlite3

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
    
    # load URL endpoints file
    def load_endpoints(self):
        try: 
            file = open(self.file_endpoints)
            self.endpoints = json.load(file)
            
            print(f'ESI endpoints loaded')
        except Exception as e:
            print(f'ESI endpoints NOT loaded: {e}')
    
    # get the old sde checksum
    def load_old_checksum(self):
        try:
            file = open(self.file_checksum)
            self.checksum = file.read()
            
            print(f'SDE old checksum is: {self.checksum}')
            return self.checksum
        except Exception as e:
            print(f'SDE checksum NOT loaded: {e}')            
    
    # get the new sde checksum
    def load_new_checksum(self):
        try:
            sde_checksum_url = self.endpoints['sde_checksum_url']
            response = requests.get(sde_checksum_url)
            if response.status_code == 200:
                print(f'SDE new checksum is: {response.text}')
                return response.text
            else:
                print(f'WARNING: HTTP response code not 200!')
                return ''
        except Exception as e:
            print(f'failed to get new SDE checksum: {e}')
            
    # is checksum changed?   
    def validate_sde_hash(self):        
        old_checksum = self.load_old_checksum()
        new_checksum = self.load_new_checksum()
        
        if old_checksum != new_checksum:
            print(f'SDE checksum NOT matched!')
        else: 
            print(f'SDE checksum match')    
            
    def run(self):
        #load endpoints
        self.load_endpoints()
        
        #check SDE hash 
        self.validate_sde_hash()    
            
if __name__ == '__main__':
    Main().run()
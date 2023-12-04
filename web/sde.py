import os
import log
import traceback

from web.web import web

class sde:
    
    def __init__(self):
        self.sde_hash = 'sde_checksum'
        self.sde_local_path = 'sde/'
        self.sde_hash_url = ''
        self.sde_url = ''
    
    # download new SDE zips if nessesary
    def sde_update(self):
        if(self.is_sde_hash_obsolete):
            return
        
    
    
    # fetch local saved sde hash (if exists)
    def sde_hash_old_load(self):
        try:
            file = open(self.sde_hash)
            checksum = file.read()
            file.close()
            return checksum
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')
            return ''
    
    
    # fetch current hash from url
    def sde_hash_new_get(self):
        try:
            checksum = web.http_get(self.sde_hash_url)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')
        
    
    # check if sde hash is obsolete
    def is_sde_hash_obsolete(self):
        try:
            old = self.sde_hash_old_load()
            new = self.sde_hash_new_get()
            if (old==new):
                return True
            return False
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')
            return False
        
    
    # cleanup old sde
    def sde_cleanup(self):
        blah = 123 #TODO
        
        
    # sde download
    def sde_download(self):
        blah = 123 #TODO
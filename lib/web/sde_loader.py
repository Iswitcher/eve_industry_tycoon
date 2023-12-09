import os
import zipfile
import shutil
import traceback

from lib.logger import logger
from lib.cfg_reader import cfg_reader
from lib.web.web import web


class sde_loader:
    
    def __init__(self):
        self.log = logger()
        self.cfg = cfg_reader()
        self.sde_config_path = 'config/sde_import.json'
        self.sde_endpoints = {}

        self.sde_hash = 'sde_checksum.txt'
        self.sde_folder = 'sde/'
        self.sde_zip_path = 'sde/sde.zip'
        
    
    # main method. Checks and downloads new SDE archive
    def sde_update(self):
        try:
            self.sde_config_get()
            old_hash = self.sde_hash_old_load()
            new_hash = self.sde_hash_new_get()
            if(self.is_sde_hash_obsolete(old_hash, new_hash)):
                return
            self.sde_download_zip()
            self.sde_hash_new_save(new_hash)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')

    
    # get sde config JSON
    def sde_config_get(self):
        self.sde_endpoints = self.cfg.get_config_json(self.sde_config_path)
        
    
    # fetch local saved sde hash (if exists)
    def sde_hash_old_load(self):
        try:
            file = open(self.sde_hash)
            checksum = file.read()
            file.close()
            return checksum
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            return ''
    
    
    # fetch current hash from url
    def sde_hash_new_get(self):
        try:
            url = self.sde_endpoints.sde_checksum_url
            checksum = web.http_get(url)
            return checksum
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
        
    
    # check if sde hash is obsolete
    def is_sde_hash_obsolete(self, old, new):
        try:
            if (old==new):
                return True
            return False
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            return False
           
        
    # save the checksum
    def sde_hash_new_save(self, checksum):
        try:
            file = open(self.sde_hash, "w")
            checksum = file.write(checksum)
            file.close()
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
        
        
    # sde download
    def sde_download_zip(self):
        try:
            url = self.sde_endpoints.sde_download_url
            data = web.http_get_bytes(url)
            self.sde_dir_check()
            self.sde_dir_clean()
            with zipfile.ZipFile(data, 'r') as zip:
                zip.extractall('')
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
            
    # create sde dir if not exists
    def sde_dir_check(self):
        if not os.path.exists(self.sde_folder):
            os.makedirs(self.sde_folder)
            
            
    # clean old SDE folder if needed
    def sde_dir_clean(self):
        try:
            if os.path.exists(self.sde_folder):
                shutil.rmtree(self.sde_folder)
                return
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
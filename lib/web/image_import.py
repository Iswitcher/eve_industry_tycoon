import re
import os
import shutil
import zipfile
import traceback

from lib.cfg_reader import cfg_reader
from lib.web.http import http

class image_import:
    
    def __init__(self, log):
        self.log = log
        self.cfg = cfg_reader()
        self.http = http(log)
        self.config_path = 'config/image_import.json'
        self.config = {}


    def get_config(self):
        try:
            self.config = self.cfg.get_config_json(self.config_path)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    def get_icons(self):
        try:
            self.get_config()
            sde_page = str(self.get_sde_page())
            objects = self.config.graphic_flies
            for obj in objects:
                r = re.compile(obj.url_regex)
                match = re.search(r, sde_page)
                url = match.group(0)
                path = obj.res_path
                self.log.info(f'downloading {url}')
                self.load_zip(url, path)    
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    def get_sde_page(self):
        try:
            url = self.config.sde_page_url
            page = self.http.http_get(url)
            return page
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    def load_zip(self, url, path):
        try:
            data = self.http.http_get_bytes(url)
            self.dir_check(path)
            self.dir_clean(path)
            with zipfile.ZipFile(data, 'r') as zip:
                zip.extractall(path)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # create dir if not exists
    def dir_check(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
            
            
    # clean old folder if needed
    def dir_clean(self, path):
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
                return
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
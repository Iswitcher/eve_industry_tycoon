from lib.web.rest import rest
from lib.logger import logger

class esi:        
    
    def __init__(self, log: logger):
        self.log = log
        self.esi_endpoints_path = 'config/esi_endpoints.json'
        self.esi_endpoints = {}


    def esi_test(self):
        result = self.market_get_region_types()
        return result


    def market_get_region_types(self):
        base = 'https://esi.evetech.net/latest/'
        region = '10000002'
        params = {}
        params['datasource'] = 'tranquility'
        
        url = f'{base}markets/{region}/types/'
        result = rest.get(self, url=url, params=params)
        return result
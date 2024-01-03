from lib.web.rest import rest
from lib.logger import logger

class esi:        
    
    def __init__(self, log: logger):
        self.log = log        
        self.swagger_url = 'https://esi.evetech.net/latest'


    def esi_test(self):
        region = '10000002' # The Forge
        result = self.market_get_region_types(region)
        return result


    # get default call parameters
    def esi_get_params(self):
        params = {}
        params['datasource'] = 'tranquility'
        params['language'] = 'en'
        return params


    # add parameter
    def esi_add_parameter(self, params, type, value):
        if type != None & value != None:
            params[type] = value
        return params


    # Return a list of historical market statistics for the specified type in a region
    def market_get_region_history(self, region_id, type_id=None):
        url = f'{self.swagger_url}/markets/{region_id}/history/'
        params = self.esi_get_params()
        params = self.esi_add_parameter(params, 'type_id', type_id)
        
        result = rest.get(self, url=url, params=params)
        return result


    # Return a list of orders in a region
    def market_get_region_orders(self, region_id, type_id=None):      
        url = f'/markets/{region_id}/orders/'
        params = self.esi_get_params()
        params = self.esi_add_parameter(params, 'type_id', type_id)
        
        result = rest.get(self, url=url, params=params)
        return result


    # Return a list of type IDs that have active orders in the region
    def market_get_region_types(self, region_id):
        url = f'{self.swagger_url}/markets/{region_id}/types/'
        params = self.esi_get_params()
        
        result = rest.get(self, url=url, params=params)
        return result


    # Get a list of item groups
    def market_get_groups(self):
        url = f'{self.swagger_url}/markets/groups/'
        params = self.esi_get_params()
        
        result = rest.get(self, url=url, params=params)
        return result


    # Get information on an item group
    def market_get_group_info(self, market_group_id):
        url = f'{self.swagger_url}/markets/groups/{market_group_id}/'
        params = self.esi_get_params()
        
        result = rest.get(self, url=url, params=params)
        return result


    # Return a list of prices
    def market_get_group_info(self):
        url = f'{self.swagger_url}/markets/prices/'
        params = self.esi_get_params()
        
        result = rest.get(self, url=url, params=params)
        return result
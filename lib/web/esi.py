from lib.web.rest import rest
from lib.logger import logger

class esi:        
    
    def __init__(self, log: logger):
        self.log = log        
        self.swagger_url = 'https://esi.evetech.net/latest'


    def esi_test(self):
        regions = self.universe_get_regions()
        region = '10000002' # The Forge
        region_info = self.universe_get_region_info(region)
        
        constelations = self.universe_get_constelations()
        constelation = '20000020' # Kimotoro
        constelation_info = self.universe_get_constelation_info(constelation)
        
        systems = self.universe_get_systems()
        system = '30000142' # Jita
        system_info = self.universe_get_system_info(system)
        
        stargate = '50001249' # Stargate (Perimeter)
        stargate_info = self.universe_get_stargate_info(stargate)
        
        station = '60003760' # Jita IV - Moon 4 - Caldari Navy Assembly Plant
        sstation_info = self.universe_get_station_info(station)
        
        dummy = self.market_get_region_types(region)
        
        return ''

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


    # ==================
    # MARKET
    # ==================
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

    # ==================
    # UNIVERSE
    # ==================
    # Get a list of regions
    def universe_get_regions(self):
        url = f'{self.swagger_url}/universe/regions/'
        params = self.esi_get_params()
        
        result = rest.get(self, url=url, params=params)
        return result


    # Get information on a region
    def universe_get_region_info(self, region_id):
        url = f'{self.swagger_url}/universe/regions/{region_id}/'
        params = self.esi_get_params()
        
        result = rest.get(self, url=url, params=params)
        return result


    # Get a list of constellations
    def universe_get_constelations(self):
        url = f'{self.swagger_url}/universe/constellations/'
        params = self.esi_get_params()
        
        result = rest.get(self, url=url, params=params)
        return result


    # Get information on a constellation
    def universe_get_constelation_info(self, constellation_id):
        url = f'{self.swagger_url}/universe/constellations/{constellation_id}/'
        params = self.esi_get_params()
        
        result = rest.get(self, url=url, params=params)
        return result


    # Get a list of systems
    def universe_get_systems(self):
        url = f'{self.swagger_url}/universe/systems/'
        params = self.esi_get_params()
        
        result = rest.get(self, url=url, params=params)
        return result


    # Get information on a system
    def universe_get_system_info(self, system_id):
        url = f'{self.swagger_url}/universe/systems/{system_id}/'
        params = self.esi_get_params()
        
        result = rest.get(self, url=url, params=params)
        return result


    # Get information on a stargate
    def universe_get_stargate_info(self, stargate_id):
        url = f'{self.swagger_url}/universe/stargates/{stargate_id}/'
        params = self.esi_get_params()
        
        result = rest.get(self, url=url, params=params)
        return result


    # Get information on a station
    def universe_get_station_info(self, station_id):
        url = f'{self.swagger_url}/universe/stations/{station_id}/'
        params = self.esi_get_params()
        
        result = rest.get(self, url=url, params=params)
        return result


    # TODO: public (?) structure list
    # TODO: structure info (needs char auth token)

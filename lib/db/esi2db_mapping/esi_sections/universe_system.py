import traceback

from lib.db.esi2db_mapping.esi_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class universe_system(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.systems = table_systems()
        self.planets = table_system_planets()
        self.moons = table_system_planet_moons()
        self.stargates = table_system_stargates()
        self.stations = table_system_stations()


    # check if all tables are present
    def check(self):
        try:
            # systems
            self.check_table(self.systems)
            
            # system_planets
            self.check_table(self.planets)
            
            # system_moons
            self.check_table(self.moons)
            
            # system_stargates
            self.check_table(self.stargates)
            
            # system_stations
            self.check_table(self.stations)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.systems.table_name)
            self.db.table_start_sync(self.planets.table_name)
            self.db.table_start_sync(self.moons.table_name)
            self.db.table_start_sync(self.stargates.table_name)
            self.db.table_start_sync(self.stations.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # add new row
    def run(self, row):
        try:
            self.add_system(self.systems, row)
            self.add_planets(self.planets, row)
            # self.add_moons(self.moons, row)
            self.add_stargates(self.stargates, row)
            self.add_stations(self.stations, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.systems.table_name)
            self.db.table_finish_sync(self.planets.table_name)
            self.db.table_finish_sync(self.moons.table_name)
            self.db.table_finish_sync(self.stargates.table_name)
            self.db.table_finish_sync(self.stations.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}') 


    # add system
    def add_system(self, table_obj, row):
        try:
            columns = []
            values = []
            id = self.json_value_get(row, table_obj.table_pk)
            for column in table_obj.columns:
                value = self.json_value_get(row, column.path)
                if value == None:
                    continue
                columns.append(column.name)
                values.append(value)
            table = table_obj.table_name
            pk = table_obj.table_pk
            self.db.record_add_or_replace(table, pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # add planets
    def add_planets(self, table_obj, row):
        try:
            table = table_obj.table_name
            pk = table_obj.table_pk
            system_id = self.json_value_get(row, 'system_id')
            planets = self.json_value_get(row, 'planets')
            for planet in planets:
                columns = []
                values = []
                
                columns.append('system_id')
                values.append(system_id)
                
                columns.append('planet_id')
                planet_id = self.json_value_get(planet, 'planet_id')
                moon_array = self.json_value_get(planet, 'moons')
                if moon_array is not None:
                    self.add_planet_moons(self.moons, moon_array, planet_id, system_id)
                values.append(planet_id)
                self.db.record_add_or_replace(table, pk, system_id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # add planet moons
    def add_planet_moons(self, table_obj, moons, planet_id, system_id):
        try:
            table = table_obj.table_name
            pk = table_obj.table_pk
            for moon in moons:
                columns = []
                values = []
                
                columns.append('system_id')
                values.append(system_id)
                
                columns.append('planet_id')
                values.append(planet_id)
                
                columns.append('moon_id')
                values.append(moon)
                self.db.record_add_or_replace(table, pk, system_id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')

    # add stargates
    def add_stargates(self, table_obj, row):
        try:
            table = table_obj.table_name
            pk = table_obj.table_pk
            system_id = self.json_value_get(row, 'system_id')
            stargates = self.json_value_get(row, 'stargates')
            for stargate in stargates:
                columns = []
                values = []
                
                columns.append('system_id')
                values.append(system_id)
                
                columns.append('stargate_id')
                values.append(stargate)
                self.db.record_add_or_replace(table, pk, system_id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # add stations
    def add_stations(self, table_obj, row):
        try:
            table = table_obj.table_name
            pk = table_obj.table_pk
            system_id = self.json_value_get(row, 'system_id')
            stations = self.json_value_get(row, 'stations')
            for station in stations:
                columns = []
                values = []
                
                columns.append('system_id')
                values.append(system_id)
                
                columns.append('station_id')
                values.append(station)
                self.db.record_add_or_replace(table, pk, system_id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


class col:
    def __init__(self, name, type = 'TEXT', path = None):
        self.name = name
        self.type = type
        self.path = path
    

class table_systems:
    def __init__(self):
        self.table_name = 'universe_systems'
        self.table_pk = 'system_id'
        self.columns = []
        
        self.columns.append(col('system_id',        'NUMBER', 'system_id'))
        self.columns.append(col('constellation_id', 'NUMBER', 'constellation_id'))
        self.columns.append(col('name',             'TEXT', 'name'))
        self.columns.append(col('security_class',   'TEXT', 'security_class'))
        self.columns.append(col('security_status',  'NUMBER', 'security_status'))
        self.columns.append(col('star_id',          'NUMBER', 'star_id'))
        self.columns.append(col('pos_x',            'NUMBER', 'position/x'))
        self.columns.append(col('pos_y',            'NUMBER', 'position/y'))
        self.columns.append(col('pos_z',            'NUMBER', 'position/z'))


class table_system_planets:
    def __init__(self):
        self.table_name = 'universe_system_planets'
        self.table_pk = 'system_id'
        self.columns = []
        
        self.columns.append(col('system_id',    'NUMBER', 'system_id'))
        self.columns.append(col('planet_id',    'NUMBER', ''))


class table_system_planet_moons:
    def __init__(self):
        self.table_name = 'universe_system_planet_moons'
        self.table_pk = 'system_id'
        self.columns = []
        
        self.columns.append(col('system_id',    'NUMBER', 'system_id'))
        self.columns.append(col('planet_id',    'NUMBER', ''))
        self.columns.append(col('moon_id',      'NUMBER', ''))


class table_system_stargates:
    def __init__(self):
        self.table_name = 'universe_system_stargates'
        self.table_pk = 'system_id'
        self.columns = []
        
        self.columns.append(col('system_id',    'NUMBER', 'system_id'))
        self.columns.append(col('stargate_id',  'NUMBER', ''))


class table_system_stations:
    def __init__(self):
        self.table_name = 'universe_system_stations'
        self.table_pk = 'system_id'
        self.columns = []
        
        self.columns.append(col('system_id',    'NUMBER', 'system_id'))
        self.columns.append(col('station_id',   'NUMBER', ''))
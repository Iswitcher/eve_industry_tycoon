import traceback

from lib.db.esi2db_mapping.esi_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class universe_constellation(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.constellations = table_constellations()
        self.systems = table_constellation_constellations()


    # check if all tables are present
    def check(self):
        try:
            # constellations
            self.check_table(self.constellations)
            
            # constellation_systems
            self.check_table(self.systems)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.constellations.table_name)
            self.db.table_start_sync(self.systems.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # add new row
    def run(self, row):
        try:
            self.add_constellation(self.constellations, row)
            self.add_system(self.systems, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.constellations.table_name)
            self.db.table_finish_sync(self.systems.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}') 


    # add constellation
    def add_constellation(self, table_obj, row):
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


    # add system
    def add_system(self, table_obj, row):
        try:
            table = table_obj.table_name
            pk = table_obj.table_pk
            constellation_id = self.json_value_get(row, 'constellation_id')
            constellations = self.json_value_get(row, 'systems')
            for c in constellations:
                columns = []
                values = []
                
                columns.append('constellation_id')
                values.append(constellation_id)
                
                columns.append('system_id')
                values.append(c)
                self.db.record_add_or_replace(table, pk, constellation_id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


class col:
    def __init__(self, name, type = 'TEXT', path = None):
        self.name = name
        self.type = type
        self.path = path
    

class table_constellations:
    def __init__(self):
        self.table_name = 'universe_constellations'
        self.table_pk = 'constellation_id'
        self.columns = []
        
        self.columns.append(col('region_id',        'NUMBER', 'region_id'))
        self.columns.append(col('constellation_id', 'NUMBER', 'constellation_id'))
        self.columns.append(col('name',             'TEXT', 'name'))
        self.columns.append(col('pos_x',            'NUMBER', 'position/x'))
        self.columns.append(col('pos_y',            'NUMBER', 'position/y'))
        self.columns.append(col('pos_z',            'NUMBER', 'position/z'))


class table_constellation_constellations:
    def __init__(self):
        self.table_name = 'universe_constellation_systems'
        self.table_pk = 'constellation_id'
        self.columns = []
        
        self.columns.append(col('constellation_id', 'NUMBER', 'constellation_id'))
        self.columns.append(col('system_id',        'NUMBER', ''))
import traceback

from lib.db.esi2db_mapping.esi_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class universe_region(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.regions = table_regions()
        self.constellations = table_region_constellations()


    # check if all tables are present
    def check(self):
        try:
            # regions
            self.check_table(self.regions)
            
            # region_constellations
            self.check_table(self.constellations)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.regions.table_name)
            self.db.table_start_sync(self.constellations.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # add new row
    def run(self, row):
        try:
            self.add_region(self.regions, row)
            self.add_constellations(self.constellations, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.regions.table_name)
            self.db.table_finish_sync(self.constellations.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}') 


    # add region
    def add_region(self, table_obj, row):
        try:
            columns = []
            values = []
            
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


    # add constellation
    def add_constellations(self, table_obj, row):
        try:
            table = table_obj.table_name
            pk = table_obj.table_pk
            region_id = self.json_value_get(row, 'region_id')
            constellations = self.json_value_get(row, 'constellations')
            for c in constellations:
                columns = []
                values = []
                
                columns.append('region_id')
                values.append(region_id)
                
                columns.append('constellation_id')
                values.append(c)
                self.db.record_add_or_replace(table, pk, region_id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


class col:
    def __init__(self, name, type = 'TEXT', path = None):
        self.name = name
        self.type = type
        self.path = path
    

class table_regions:
    def __init__(self):
        self.table_name = 'universe_regions'
        self.table_pk = 'region_id'
        self.columns = []
        
        self.columns.append(col('region_id',    'NUMBER', 'region_id'))
        self.columns.append(col('name',         'TEXT', 'name'))
        self.columns.append(col('description',  'TEXT', 'description'))


class table_region_constellations:
    def __init__(self):
        self.table_name = 'universe_region_constellations'
        self.table_pk = 'region_id'
        self.columns = []
        
        self.columns.append(col('region_id',        'NUMBER', 'region_id'))
        self.columns.append(col('constellation_id', 'NUMBER', ''))
import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class agents(mapper):
    
    def __init__(self, db, log):
        self.db = db
        self.log = log
        self.agents = table_agents()
        
        

    # check if all tables are present
    def check(self):
        try:
            # agents
            blah = self.agents.columns
            agent_cols = [], agent_types = []
            for column in self.agents.columns:
                agent_cols.append(column.name)
                agent_types.append(column.type)
                blah = 123
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')

    
    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.table_agents)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            

    # add new row
    def run(self, id, row):
        try:
            self.add_agent(self.table_agents, self.table_agents_pk, id, row) 
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.table_agents)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # get the list of columns in table: agents
    def get_agent_columns(self, columns = [], types = []):
        columns.append('agent_id')
        types.append('NUMBER')
        
        columns.append('agent_type_id')
        types.append('NUMBER')
        
        columns.append('corporation_id')
        types.append('NUMBER')
        
        columns.append('division_id')
        types.append('NUMBER')
        
        columns.append('is_locator')
        types.append('NUMBER')
        
        columns.append('level')
        types.append('NUMBER')
        
        columns.append('location_id')
        types.append('NUMBER')
        
        return columns, types    
         
    
    # add or update an agent        
    def add_agent(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            columns.append('agent_id')
            values.append(id)
            
            columns.append('agent_type_id')
            values.append(self.yaml_value_extract(row, 'agentTypeID'))
            
            columns.append('corporation_id')
            values.append(self.yaml_value_extract(row, 'corporationID'))
            
            columns.append('division_id')
            values.append(self.yaml_value_extract(row, 'divisionID'))
            
            columns.append('is_locator')
            values.append(self.yaml_value_extract(row, 'isLocator'))
            
            columns.append('level')
            values.append(self.yaml_value_extract(row, 'level'))
            
            columns.append('location_id')
            values.append(self.yaml_value_extract(row, 'locationID'))
            
            self.db.record_add_or_replace(table, pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
class col:
    def __init__(self, name, type = 'TEXT', path = None):
        self.name = name
        self.type = type
        self.path = path
    

class table_agents:
    def __init__(self):
        self.table_name = 'agents'
        self.table_pk = 'agent_id'
        self.columns = []
        
        self.columns.append(col('agent_id',       'NUMBER', '#root'))
        self.columns.append(col('agent_type_id',  'NUMBER', 'agentTypeID'))
        self.columns.append(col('corporation_id', 'NUMBER', 'corporationID'))
        self.columns.append(col('division_id',    'NUMBER', 'divisionID'))
        self.columns.append(col('is_locator',     'NUMBER', 'isLocator'))
        self.columns.append(col('level',          'NUMBER', 'level'))
        self.columns.append(col('location_id',    'NUMBER', 'locationID'))
        

        
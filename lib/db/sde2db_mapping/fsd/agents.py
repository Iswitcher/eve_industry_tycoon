import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class agents(mapper):
    
    def __init__(self, db_path, yaml):
        self.db_path = db_path
        self.yaml = yaml
        self.db = db_utils(self.db_path, None)
        self.log = logger()
        
        self.table_agents = 'agents'
        self.table_agents_pk = 'agent_id'


    def run(self):
        try:
            self.db.db_check()
            self.db.db_connect()
            
            self.check_tables_and_columns()
            self.sync_start()
            for row in self.yaml:
                # add row to agents table
                self.add_agent(self.table_agents, self.table_agents_pk, row, self.yaml[row]) 
            self.sync_end()
            self.db.db_disconnect()
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
    
    # check if table exists
    def check_table(self, table):
        try:
            if not self.db.table_check(table):
                self.db.table_create(table)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    # check all class-cpecific tables and columns
    def check_tables_and_columns(self):
        try:
            # agents
            self.check_table(self.table_agents)
            agent_columns, agent_types = self.get_agent_columns()
            self.db.table_column_check(self.table_agents, agent_columns, agent_types)  
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
    
    # prepare for sync
    def sync_start(self):
        try:
            self.db.table_start_sync(self.table_agents)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    # complete the sync
    def sync_end(self):
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
            values.append(row['agentTypeID'])
            
            columns.append('corporation_id')
            values.append(row['corporationID'])
            
            columns.append('division_id')
            values.append(row['divisionID'])
            
            columns.append('is_locator')
            values.append(row['isLocator'])
            
            columns.append('level')
            values.append(row['level'])
            
            columns.append('location_id')
            values.append(row['locationID'])
            
            self.db.record_add_or_replace(table, pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    


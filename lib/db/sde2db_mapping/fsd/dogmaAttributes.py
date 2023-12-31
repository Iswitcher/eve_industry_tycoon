import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class dogmaAttributes(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.attributes = table_attributes()
        
    
    # check if all tables are present
    def check(self):
        try:
            # dogmaAttributeCategories
            self.check_table(self.attributes)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.attributes.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_activity(self.attributes.table_name, self.attributes.table_pk, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.attributes.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update a attribute        
    def add_activity(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            for column in self.attributes.columns:
                value = self.yaml_value_extract(id, row, column.path)
                columns.append(column.name)
                values.append(value)
            self.db.record_add_or_replace(table, pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
        

class col:
    def __init__(self, name, type = 'TEXT', path = None):
        self.name = name
        self.type = type
        self.path = path
    

class table_attributes:
    def __init__(self):
        self.table_name = 'attributes'
        self.table_pk = 'attribute_id'
        self.columns = []
        
        self.columns.append(col('attribute_id',     'NUMBER', '#root'))
        self.columns.append(col('max_attribute_id', 'NUMBER', 'maxAttributeID'))
        self.columns.append(col('category_id',      'NUMBER', 'categoryID'))
        self.columns.append(col('charge_recharge_time_id',  'NUMBER', 'chargeRechargeTimeID'))
        self.columns.append(col('data_type',        'NUMBER', 'dataType'))
        self.columns.append(col('default_value',    'NUMBER', 'defaultValue'))
        self.columns.append(col('unit_id',          'NUMBER', 'unitID'))
        self.columns.append(col('name',             'TEXT', 'name'))
        self.columns.append(col('description',      'TEXT', 'description'))
        self.columns.append(col('display_name_en',  'TEXT', 'displayNameID/en'))
        self.columns.append(col('tooltip_title',    'TEXT', 'tooltipTitleID/en'))
        self.columns.append(col('tooltip_desc',     'TEXT', 'tooltipDescriptionID/en'))
        self.columns.append(col('high_is_good',     'TEXT', 'highIsGood'))
        self.columns.append(col('display_when_zero','TEXT', 'displayWhenZero'))
        self.columns.append(col('is_published',     'TEXT', 'published'))
        self.columns.append(col('is_stackable',     'TEXT', 'stackable'))
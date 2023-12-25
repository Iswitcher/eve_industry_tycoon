import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class typeIDs(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.types = table_types()
        self.masteries = table_masteries()
        self.trait_types = table_trait_types()
        self.trait_roles = table_trait_role_bonuses()
        self.trait_misc = table_trait_misc_bonuses()
        
    
    # check if all tables are present
    def check(self):
        try:
            # types
            self.check_table(self.types)
            
            # masteries
            self.check_table(self.masteries)
            
            # trait_types
            self.check_table(self.trait_types)
            
            # trait_roles
            self.check_table(self.trait_roles)
            
            # trait_misc
            self.check_table(self.trait_misc)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
    
    # check provided table obj
    def check_table(self, table_obj):
        try:
            if not self.db.table_check(table_obj.table_name):
                    self.db.table_create(table_obj.table_name)
            cols = [] 
            types = []
            for column in table_obj.columns:
                    cols.append(column.name)
                    types.append(column.type)
            self.db.table_column_check(table_obj.table_name, cols, types)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.types.table_name)
            self.db.table_start_sync(self.masteries.table_name)
            self.db.table_start_sync(self.trait_types.table_name)
            self.db.table_start_sync(self.trait_roles.table_name)
            self.db.table_start_sync(self.trait_misc.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.log.info(f'adding {id}')
            self.add_type(self.types, id, row)
            self.add_trait_type(self.trait_types, id, row, 'traits/types')
            self.add_trait(self.trait_roles, id, row, 'traits/roleBonuses')
            self.add_trait(self.trait_misc, id, row, 'traits/miscBonuses')
            self.add_mastery(self.masteries, id, row, 'masteries')
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.types.table_name)
            self.db.table_finish_sync(self.masteries.table_name)
            self.db.table_finish_sync(self.trait_types.table_name)
            self.db.table_finish_sync(self.trait_roles.table_name)
            self.db.table_finish_sync(self.trait_misc.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update types   
    def add_type(self, table_obj, id, row):
        try:
            t_name = table_obj.table_name
            t_pk = table_obj.table_pk
            columns = []
            values = []
            for column in table_obj.columns:
                value = self.yaml_value_extract(id, row, column.path)
                columns.append(column.name)
                values.append(value)
            self.db.record_add_or_replace(t_name, t_pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    def add_trait(self, table_obj, id, row, node):
        try:
            t_name = table_obj.table_name
            t_pk = table_obj.table_pk
            data = self.yaml_value_extract(id, row, node)
            if data == None:
                return
            for item in data:
                columns = []
                values = []
                for column in table_obj.columns:
                    value = self.yaml_value_extract(id, item, column.path)
                    columns.append(column.name)
                    values.append(value)
                self.db.record_add_or_replace(t_name, t_pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
    
    def add_trait_type(self, table_obj, id, row, node):
        try:
            t_name = table_obj.table_name
            t_pk = table_obj.table_pk
            data = self.yaml_value_extract(id, row, node)
            if data == None:
                return
            for trait in data:
                for item in data[trait]:
                    columns = []
                    values = []
                    for column in table_obj.columns:
                        value = self.yaml_value_extract(id, item, column.path)
                        if column.name == 'trait_type_id':
                            value = trait
                        columns.append(column.name)
                        values.append(value)
                    self.db.record_add_or_replace(t_name, t_pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
            
    def add_mastery(self, table_obj, id, row, node):
        try:
            t_name = table_obj.table_name
            t_pk = table_obj.table_pk
            data = self.yaml_value_extract(id, row, node)
            if data == None:
                return
            for level in data:
                for item in data[level]:
                    columns = []
                    values = []
                    for column in table_obj.columns:
                        if column.name == 'type_id':
                            value = id
                        if column.name == 'level':
                            value = level
                        if column.name == 'mastery_id':
                            value = item
                        columns.append(column.name)
                        values.append(value)
                    self.db.record_add_or_replace(t_name, t_pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
        
class col:
    def __init__(self, name, type = 'TEXT', path = None):
        self.name = name
        self.type = type
        self.path = path
    

class table_types:
    def __init__(self):
        self.table_name = 'types'
        self.table_pk = 'type_id'
        self.columns = []
        
        self.columns.append(col('type_id',          'NUMBER', '#root'))
        self.columns.append(col('name_en',          'TEXT', 'name/en'))
        self.columns.append(col('description_en',   'TEXT', 'description/en'))
        self.columns.append(col('base_price',       'NUMBER', 'basePrice'))
        self.columns.append(col('graphic_id',       'NUMBER', 'graphicID'))
        self.columns.append(col('group_id',         'NUMBER', 'groupID'))
        self.columns.append(col('icon_id',          'NUMBER', 'iconID'))
        self.columns.append(col('capacity',         'NUMBER', 'capacity'))
        self.columns.append(col('meta_group_id',    'NUMBER', 'metaGroupID'))
        self.columns.append(col('market_group_id',  'NUMBER', 'marketGroupID'))
        self.columns.append(col('mass',             'NUMBER', 'mass'))
        self.columns.append(col('portion_size',     'NUMBER', 'portionSize'))
        self.columns.append(col('is_published',     'TEXT', 'published'))
        self.columns.append(col('race_id',          'NUMBER', 'raceID'))
        self.columns.append(col('radius',           'NUMBER', 'radius'))
        self.columns.append(col('sof_faction_name', 'TEXT', 'sofFactionName'))
        self.columns.append(col('sound_id',         'NUMBER', 'soundID'))
        self.columns.append(col('variation_parent_type_id', 'NUMBER', 'variationParentTypeID'))
        self.columns.append(col('volume',           'NUMBER', 'volume'))
        self.columns.append(col('faction_id',       'NUMBER', 'factionID'))
        self.columns.append(col('sof_material_set_id', 'NUMBER', 'sofMaterialSetID'))


class table_masteries:
    def __init__(self):
        self.table_name = 'types_masteries'
        self.table_pk = 'type_id'
        self.columns = []
        
        self.columns.append(col('type_id',      'NUMBER', '#root'))
        self.columns.append(col('level',        'NUMBER', ''))
        self.columns.append(col('mastery_id',   'NUMBER', '')) #TODO: check the naming
        

class table_trait_types:
    def __init__(self):
        self.table_name = 'types_trait_types'
        self.table_pk = 'type_id'
        self.columns = []   
        
        self.columns.append(col('type_id',      'NUMBER', '#root'))
        self.columns.append(col('trait_type_id','NUMBER', ''))
        self.columns.append(col('bonus',        'NUMBER', 'bonus'))
        self.columns.append(col('bonus_text_en','NUMBER', 'bonusText/en'))
        self.columns.append(col('importance',   'NUMBER', 'importance'))
        self.columns.append(col('unit_id',      'NUMBER', 'unitID'))
        

class table_trait_role_bonuses:
    def __init__(self):
        self.table_name = 'types_trait_role_bonuses'
        self.table_pk = 'type_id'
        self.columns = []   
        
        self.columns.append(col('type_id',      'NUMBER', '#root'))
        self.columns.append(col('bonus',        'NUMBER', 'bonus'))
        self.columns.append(col('bonus_text_en','NUMBER', 'bonusText/en'))
        self.columns.append(col('importance',   'NUMBER', 'importance'))
        self.columns.append(col('unit_id',      'NUMBER', 'unitID'))
        
        
class table_trait_misc_bonuses:
    def __init__(self):
        self.table_name = 'types_trait_misc_bonuses'
        self.table_pk = 'type_id'
        self.columns = []   
        
        self.columns.append(col('type_id',      'NUMBER', '#root'))
        self.columns.append(col('bonus',        'NUMBER', 'bonus'))
        self.columns.append(col('bonus_text_en','NUMBER', 'bonusText/en'))
        self.columns.append(col('importance',   'NUMBER', 'importance'))
        self.columns.append(col('unit_id',      'NUMBER', 'unitID'))
        
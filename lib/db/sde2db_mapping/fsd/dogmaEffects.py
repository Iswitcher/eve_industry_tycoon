import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class dogmaEffects(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.effects = table_effects()
        self.modifiers = table_modifiers()
        
    
    # check if all tables are present
    def check(self):
        try:
            # dogmaEffects
            self.check_table(self.effects)
            
            # modifiers
            self.check_table(self.modifiers)
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
            self.db.table_start_sync(self.effects.table_name)
            self.db.table_start_sync(self.modifiers.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_effect(self.effects.table_name, self.effects.table_pk, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.effects.table_name)
            self.db.table_finish_sync(self.modifiers.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update a effect        
    def add_effect(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            for column in self.effects.columns:
                value = self.yaml_value_extract(id, row, column.path)
                columns.append(column.name)
                values.append(value)
            self.db.record_add_or_replace(table, pk, id, columns, values)
            
            self.add_modifiers(self.modifiers.table_name, pk, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
            
    def add_modifiers(self, table, pk, id, row):
        try:
            data = self.yaml_value_extract(id, row, 'modifierInfo')
            if data == None:
                return
            for modifier in data:
                columns = []
                values = []
                for column in self.modifiers.columns:
                    value = self.yaml_value_extract(id, modifier, column.path)
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
    

class table_effects:
    def __init__(self):
        self.table_name = 'effects'
        self.table_pk = 'effect_id'
        self.columns = []
        
        self.columns.append(col('effect_id',                    'NUMBER', '#root'))
        self.columns.append(col('disallow_auto_repeat',         'TEXT', 'disallowAutoRepeat'))
        self.columns.append(col('discharge_attribute_id',       'NUMBER', 'dischargeAttributeID'))
        self.columns.append(col('duration_attribute_id',        'NUMBER', 'durationAttributeID'))
        self.columns.append(col('falloff_attribute_id',         'NUMBER', 'falloffAttributeID'))
        self.columns.append(col('tracking_attribute_id',        'NUMBER', 'trackingSpeedAttributeID'))
        self.columns.append(col('resistance_attribute_id',      'NUMBER', 'resistanceAttributeID'))
        self.columns.append(col('distribution',                 'NUMBER', 'distribution'))
        self.columns.append(col('effect_category',              'NUMBER', 'effectCategory'))
        self.columns.append(col('effect_id',                    'NUMBER', 'effectID'))
        self.columns.append(col('effect_name',                  'TEXT', 'effectName'))
        self.columns.append(col('effect_desc',                  'TEXT', 'descriptionID/en'))
        self.columns.append(col('guid',                         'TEXT', 'guid'))
        self.columns.append(col('icon_id',                      'NUMBER', 'iconID'))
        self.columns.append(col('fitting_usage_chance_att_id',  'TEXT', 'fittingUsageChanceAttributeID'))
        self.columns.append(col('npc_activation_chance_att_id', 'TEXT', 'npcActivationChanceAttributeID'))
        self.columns.append(col('npc_usage_chance_att_id',      'TEXT', 'npcUsageChanceAttributeID'))
        self.columns.append(col('electronic_chance',            'TEXT', 'electronicChance'))
        self.columns.append(col('is_assistance',                'TEXT', 'isAssistance'))
        self.columns.append(col('is_offensive',                 'TEXT', 'isOffensive'))
        self.columns.append(col('is_warp_safe',                 'TEXT', 'isWarpSafe'))
        self.columns.append(col('is_propulsion_chance',         'TEXT', 'propulsionChance'))
        self.columns.append(col('is_published',                 'TEXT', 'published'))
        self.columns.append(col('range_attribute_id',           'NUMBER', 'rangeAttributeID'))
        self.columns.append(col('is_range_chance',              'TEXT', 'rangeChance'))
        self.columns.append(col('sfx_name',                     'TEXT', 'sfxName'))
        
        
class table_modifiers:
    def __init__(self):
        self.table_name = 'effect_modifiers'
        self.table_pk = 'effect_id'
        self.columns = []
        
        self.columns.append(col('effect_id',             'NUMBER', '#root'))
        self.columns.append(col('domain',                'TEXT', 'domain'))
        self.columns.append(col('func',                  'TEXT', 'func'))
        self.columns.append(col('group_id',              'NUMBER', 'groupID'))
        self.columns.append(col('modifier_attribute_id', 'NUMBER', 'modifiedAttributeID'))
        self.columns.append(col('modifying_attribute_id','NUMBER', 'modifyingAttributeID'))
        self.columns.append(col('operation',             'NUMBER', 'operation'))
        self.columns.append(col('skill_type_id',         'NUMBER', 'skillTypeID'))
import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class npcCorporations(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.npc_corps = table_npc_corps()
        self.races = table_allowed_races()
        self.divisions = table_divisions()
        self.trades = table_trades()
        self.lp_offers = table_lp_offer()
        
    
    # check if all tables are present
    def check(self):
        try:
            # npc_corps
            self.check_table(self.npc_corps)
            
            # races
            self.check_table(self.races)
            
            # divisions
            self.check_table(self.divisions)
            
            # trades
            self.check_table(self.trades)
            
            # lp_offer
            self.check_table(self.lp_offers)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.npc_corps.table_name)
            self.db.table_start_sync(self.races.table_name)
            self.db.table_start_sync(self.divisions.table_name)
            self.db.table_start_sync(self.trades.table_name)
            self.db.table_start_sync(self.lp_offers.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_npc_corp(self.npc_corps.table_name, self.npc_corps.table_pk, id, row)
            self.add_races(self.races, id, row)
            self.add_divisions(self.divisions, id, row)
            self.add_trade(self.trades, id, row)
            self.add_lp_offers(self.lp_offers, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.npc_corps.table_name)
            self.db.table_finish_sync(self.races.table_name)
            self.db.table_finish_sync(self.divisions.table_name)
            self.db.table_finish_sync(self.trades.table_name)
            self.db.table_finish_sync(self.lp_offers.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update npc_corps   
    def add_npc_corp(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            for column in self.npc_corps.columns:
                value = self.yaml_value_extract(id, row, column.path)
                columns.append(column.name)
                values.append(value)
            self.db.record_add_or_replace(table, pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    def add_races(self, table_obj, id, row):
        try:
            data = self.yaml_value_extract(id, row, 'allowedMemberRaces')
            if data == None:
                    return
            for item in data:
                columns = []
                values = []
                for col in table_obj.columns:
                    value = self.yaml_value_extract(id, row, col.path)
                    if col.name == 'race_id':
                        value = item
                    columns.append(col.name)
                    values.append(value)    
                self.db.record_add_or_replace(table_obj.table_name, table_obj.table_pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
            
    def add_divisions(self, table_obj, id, row):
        try:
            data = self.yaml_value_extract(id, row, 'divisions')
            if data == None:
                    return
            for item in data:
                columns = []
                values = []
                for col in table_obj.columns:
                    value = self.yaml_value_extract(id, data[item], col.path)
                    if col.name == 'division_id':
                        value = item
                    columns.append(col.name)
                    values.append(value)
                self.db.record_add_or_replace(table_obj.table_name, table_obj.table_pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
            
    def add_trade(self, table_obj, id, row):
        try:
            data = self.yaml_value_extract(id, row, 'corporationTrades')
            if data == None:
                    return
            for item in data:
                columns = []
                values = []
                for col in table_obj.columns:
                    value = self.yaml_value_extract(id, row, col.path)
                    if col.name == 'type_id':
                        value = item
                    elif col.name == 'type_value':
                        value = data[item]
                    columns.append(col.name)
                    values.append(value)    
                self.db.record_add_or_replace(table_obj.table_name, table_obj.table_pk, id, columns, values)             
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
            
    def add_lp_offers(self, table_obj, id, row):
        try:
            data = self.yaml_value_extract(id, row, 'lpOfferTables')
            if data == None:
                    return
            for item in data:
                columns = []
                values = []
                for col in table_obj.columns:
                    value = self.yaml_value_extract(id, row, col.path)
                    if col.name == 'lp_offer_table':
                        value = item
                    columns.append(col.name)
                    values.append(value)    
                self.db.record_add_or_replace(table_obj.table_name, table_obj.table_pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
        
class col:
    def __init__(self, name, type = 'TEXT', path = None):
        self.name = name
        self.type = type
        self.path = path
    

class table_npc_corps:
    def __init__(self):
        self.table_name = 'npc_corps'
        self.table_pk = 'npc_corp_id'
        self.columns = []
        
        self.columns.append(col('npc_corp_id',          'NUMBER', '#root'))
        self.columns.append(col('ceo_id',               'TEXT', 'ceoID'))
        self.columns.append(col('is_deleted',           'TEXT', 'deleted'))
        self.columns.append(col('extent',               'TEXT', 'extent'))
        self.columns.append(col('has_player_personnel_manager','TEXT', 'hasPlayerPersonnelManager'))
        self.columns.append(col('initial_price',        'NUMBER', 'initialPrice'))
        self.columns.append(col('member_limit',         'NUMBER', 'memberLimit'))
        self.columns.append(col('min_security',         'NUMBER', 'minSecurity'))
        self.columns.append(col('minimum_join_standing','NUMBER', 'minimumJoinStanding'))
        self.columns.append(col('name_en',              'TEXT', 'nameID/en'))
        self.columns.append(col('desc_en',              'TEXT', 'descriptionID/en'))
        self.columns.append(col('public_shares',        'NUMBER', 'publicShares'))
        self.columns.append(col('send_char_termination_message','TEXT', 'sendCharTerminationMessage'))
        self.columns.append(col('shares',               'NUMBER', 'shares'))
        self.columns.append(col('size',                 'TEXT', 'size'))
        self.columns.append(col('station_id',           'NUMBER', 'stationID'))
        self.columns.append(col('tax_rate',             'NUMBER', 'taxRate'))
        self.columns.append(col('ticker_name',          'TEXT', 'tickerName'))
        self.columns.append(col('unique_name',          'TEXT', 'uniqueName'))
        self.columns.append(col('faction_id',           'NUMBER', 'factionID'))
        self.columns.append(col('friend_id',            'NUMBER', 'friendID'))
        self.columns.append(col('icon_id',              'NUMBER', 'iconID'))
        self.columns.append(col('main_activity_id',     'NUMBER', 'mainActivityID'))
        self.columns.append(col('race_id',              'NUMBER', 'raceID'))
        self.columns.append(col('size_factor',          'NUMBER', 'sizeFactor'))
        self.columns.append(col('solar_system_id',      'NUMBER', 'solarSystemID'))
        self.columns.append(col('secondary_activity_id','NUMBER', 'secondaryActivityID'))
        self.columns.append(col('enemy_id',             'NUMBER', 'enemyID'))


class table_allowed_races:
    def __init__(self):
        self.table_name = 'npc_corp_allowed_races'
        self.table_pk = 'npc_corp_id'
        self.columns = []
        
        self.columns.append(col('npc_corp_id','NUMBER', '#root'))
        self.columns.append(col('race_id','NUMBER', ''))


class table_divisions:
    def __init__(self):
        self.table_name = 'npc_corp_divisions'
        self.table_pk = 'npc_corp_id'
        self.columns = []
        
        self.columns.append(col('npc_corp_id',      'NUMBER', '#root'))
        self.columns.append(col('division_id',      'NUMBER', ''))
        self.columns.append(col('division_number',  'NUMBER', 'divisionNumber'))
        self.columns.append(col('leader_id',        'NUMBER', 'leaderID'))
        self.columns.append(col('size',             'NUMBER', 'size'))
        
        
class table_trades:
    def __init__(self):
        self.table_name = 'npc_corp_trades'
        self.table_pk = 'npc_corp_id'
        self.columns = []
        
        self.columns.append(col('npc_corp_id',  'NUMBER', '#root'))
        self.columns.append(col('type_id',      'NUMBER', ''))
        self.columns.append(col('type_value',   'NUMBER', ''))
        
        
class table_lp_offer:
    def __init__(self):
        self.table_name = 'npc_corp_lp_offer_tables'
        self.table_pk = 'npc_corp_id'
        self.columns = []
        
        self.columns.append(col('npc_corp_id',      'NUMBER', '#root'))
        self.columns.append(col('lp_offer_table',   'NUMBER', '#root'))
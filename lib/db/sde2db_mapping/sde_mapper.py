import traceback

from abc import ABC, abstractmethod
from lib.db.db_utils import db_utils
from lib.logger import logger

class mapper(ABC):

    # TODO: tournament rulesets?

    @abstractmethod
    def __init__(self, db: db_utils, log: logger):
        self.db = db
        self.log = log


    @abstractmethod
    def check(self):
        pass


    @abstractmethod
    def start(self):
        pass


    @abstractmethod
    def run(self):
        pass


    @abstractmethod
    def finish(self):
        pass


    # check if table and columns exist, else create
    def db_check_table(self, table, columns, types):
        if not self.db.table_check(table):
                self.db.table_create(table)
        self.db.table_column_check(table, columns, types) 


    # get yaml value by path or fill None if not found
    def yaml_value_extract(self, id, yaml_row, path):
        path_array = path.split('/')
        result = yaml_row
        try:
            for node in path_array:
                if result == None:
                    return None
                if node == '#root':
                    return id
                result = result.get(node)
            return result
        except (KeyError, TypeError):
            return None


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
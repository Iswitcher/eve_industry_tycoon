import importlib
import traceback
import json

from lib.web.esi        import esi
from lib.db.db_utils    import db_utils
from lib.logger         import logger

class esi2db:
    
    def __init__(self, log: logger):
        self.log = log
        self.db_path = 'resources/sde.db'
        self.db = db_utils(self.log, self.db_path, None, None)
        self.esi = esi(log)


    # import abstract class relevant to the object imported
    def esi_abs_class_import(self, path):
        try:
            module_path = f'lib.db.esi2db_mapping.esi_sections.{path}'
            module = importlib.import_module(module_path)
            module_class = getattr(module, path)
            module_instance = module_class(self.db, self.log)
            return module_instance
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    def esi_run_import(self, object, data):
        try:
            module = self.esi_abs_class_import(object)
            
            self.db.db_check()
            self.db.db_connect()
            
            module.check()
            module.start()
            for obj in data:
                module.run(obj)
            module.finish()
            
            self.db.db_commit()
            self.db.db_disconnect()
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # sync esi info about active regions
    def sync_universe_regions(self):
        try:
            module_path = 'universe_region'
            
            regions = self.esi.universe_get_regions()
            if regions == "":
                self.log.critical(f'No regions found')
                return
            regions = json.loads(regions)
            
            data = []
            i = 0
            for region in regions:
                i += 1
                region_info = json.loads(self.esi.universe_get_region_info(region))
                if region_info == '':
                    self.log.critical(f'CANNOT fetch region {region}. ({i}/{len(regions)})')
                    continue
                data.append(region_info)
                self.log.info(f'Region {region} fetched. ({i}/{len(regions)})')
            self.esi_run_import(module_path, data)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # sync esi info about active constellations
    def sync_universe_constellations(self):
        try:
            module_path = 'universe_constellation'
            
            constellations = self.esi.universe_get_constelations()
            if constellations == "":
                self.log.critical(f'No constellations found')
                return
            constellations = json.loads(constellations)
            
            data = []
            i = 0
            for constellation in constellations:
                i += 1
                constellation_info = json.loads(self.esi.universe_get_constellation_info(constellation))
                if constellation_info == '':
                    self.log.critical(f'CANNOT fetch constellation {constellation}. ({i}/{len(constellations)})')
                    continue
                data.append(constellation_info)
                self.log.info(f'Constellation {constellation} fetched. ({i}/{len(constellations)})')
            self.esi_run_import(module_path, data)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # sync esi info about active systems
    def sync_universe_systems(self):
        try:
            module_path = 'universe_system'
            
            systems = self.esi.universe_get_systems()
            if systems == "":
                self.log.critical(f'No systems found')
                return
            systems = json.loads(systems)
            
            data = []
            i = 0
            for system in systems:
                i += 1
                system_info = json.loads(self.esi.universe_get_system_info(system))
                if system_info == '':
                    self.log.critical(f'CANNOT fetch system {system}. ({i}/{len(systems)})')
                    continue
                data.append(system_info)
                self.log.info(f'System {system} fetched. ({i}/{len(systems)})')
            self.esi_run_import(module_path, data)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
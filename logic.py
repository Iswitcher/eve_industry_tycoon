from lib.db.sde2db          import sde2db
from lib.web.esi            import esi
from lib.web.sde_loader     import sde_loader
from lib.web.image_import   import image_import

from lib.logger import logger

class logic:

    def __init__(self, log: logger):
        self.log = log


    # try start updating SDE zips
    def sde_update(self):
        sde = sde_loader(self.log)
        sde.sde_update()


    # parse sde yaml into sqlite
    def sde_2_db(self):
        sde = sde2db(self.log)
        sde.sde_convert_all()


    def icons_download(self):
        img = image_import(self.log)
        img.get_icons()
        
        
    def esi_test(self) -> str:
        swagger = esi(self.log)
        output = swagger.esi_test()
        return output
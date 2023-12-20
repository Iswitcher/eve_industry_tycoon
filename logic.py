from lib.web.sde_loader import sde_loader
from lib.db.sde2db import sde2db

from lib.logger import logger

class logic:

    def __init__(self, logger):
        self.log = logger

    # try start updating SDE zips
    def sde_update(self):
        sde = sde_loader(self.log)
        sde.sde_update()


    # parse sde yaml into sqlite
    def sde_2_db(self):
        sde = sde2db(self.log)
        sde.sde_convert_all()

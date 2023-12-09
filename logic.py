from lib.web.sde_loader import sde_loader
from lib.db.sde2db import sde2db

class logic:
    
    # try start updating SDE zips    
    def sde_update(self):
        sde = sde_loader()
        sde.sde_update()
        
        
    # parse sde yaml into sqlite
    def sde_2_db(self):
        sde = sde2db()
        sde2db.sde_convert_all()

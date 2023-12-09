from web.sde import sde
# from web.esi import esi

# from db.sde2db import sde2db
import db.sde2db

class logic:    
    
    # try start updating SDE zips    
    def sde_update(self):
        sde_loader = sde()
        sde_loader.sde_update()
        
        
    # parse sde yaml into sqlite
    def sde_2_db(self):
        sde_loader = sde()
        checksum = sde_loader.sde_hash_old_load()
        
        conv = db.sde2db()
        conv.sde_convert_all()

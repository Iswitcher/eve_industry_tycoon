from web.sde import sde
from web.esi import esi


class logic:          
    
    # try start updating SDE zips    
    def sde_update(self):
        sde_loader = sde()
        sde_loader.sde_update()

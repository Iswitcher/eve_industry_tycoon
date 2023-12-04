from web.sde import sde

class logic:        
    
    def __init__(self, esi_endpoints):
        self.esi_endpoints = esi_endpoints
      
    
    # try start updating SDE zips    
    def sde_update(self):
        sde.sde_update(self)
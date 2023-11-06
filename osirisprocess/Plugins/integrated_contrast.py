import copy
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import dask

def integrated_contrast(self,idx_0=0,idx_f=None,idz_0=0,idz_f=None):
    efield = self.select_field["e"]["data_cyl"][f"ephi_x3_01"]
    bfield = self.select_field["b"]["data_cyl"][f"blong_x3_01"]
    nt = efield.shape[0]
    nz = efield.shape[1]
    nx = efield.shape[2]
    dx = self.dx
    dy = self.dy
    dz = self.dz
    idz_0 = np.floor(nz/2).astype(np.int32) if idz_0 == 0 else idz_0
    
    r = self.y[idz_0:idz_f]
    x = self.x[idx_0:idx_f]
    X,R = np.meshgrid(x,r)
    efield = efield[:,idz_0:idz_f,idx_0:idx_f]
    bfield = bfield[:,idz_0:idz_f,idx_0:idx_f]
    
    contrast = np.sum(R**2*np.abs(bfield)/np.abs(efield),axis=(1,2))
    
    sum_efield = np.sum(np.abs(efield),axis=(1,2))
    sum_bfield = np.sum(np.abs(bfield),axis=(1,2))
    
    sum_efield *= dz*dx
    sum_bfield *= dz*dx
    contrast *= 0.3*dx*dz
    
    return [sum_bfield.compute(),sum_efield.compute(), contrast.compute()]
    
    
    
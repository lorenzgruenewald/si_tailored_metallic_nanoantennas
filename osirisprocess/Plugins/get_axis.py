import copy
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import dask

def find_t_max(self,field,idx_0 = 0, idx_f=None, idz = None):
    '''
        Find the temporal and spatial point of maximum value for the given field.
            field: Field name to analyze (elong, ephi, erho, blong, bphi, brho)
            idx_0: Starting point to search along the propagation axis.
            idx_f: Final point to search along the propagation axis.
            idz: Point in the transverse axis to perform the search (distance from the center)
    '''
    nx = self.x.shape[0]
    ny = self.y.shape[0]
    bfield = self.select_field[field[0]]["data_cyl"][f"{field}_x3_01"]
    nt = bfield.shape[0]
    nz = bfield.shape[1]
    nx = bfield.shape[2]
    idx_f = nx if idx_f == None else idx_f
    idz = np.floor(nz/2).astype(np.int32) if idz == None else idz
    
    max_idx = np.argmax(np.abs(bfield[:,idz,idx_0:idx_f]))
    max_idx = max_idx.compute()
    max_idx = np.unravel_index(max_idx, (nt,int(idx_f-idx_0)))
    max_idx = [max_idx[0],max_idx[1]+idx_0]
    
    max_val = np.abs(bfield[max_idx[0], idz,max_idx[1]])
    max_val = max_val.compute()
    return [max_idx,max_val]

def find_max_each_x(self,field, idz = None):
    '''
        Find the the maximum value of the field in each point along the propagation axis
            field: Field name to analyze (elong, ephi, erho, blong, bphi, brho)
            idz: Point in the transverse axis to perform the search (distance from the center)
    '''
    nx = self.x.shape[0]
    ny = self.y.shape[0]
    field = self.select_field[field[0]]["data_cyl"][f"{field}_x3_01"]
    nt = field.shape[0]
    nz = field.shape[1]
    nx = field.shape[2]
    idx_0 = 0
    idx_f = None
    idz = np.floor(nz/2).astype(np.int32) if idz == None else idz
    
    max_values = np.abs(field[:, idz, :]).max(axis=0)
    max_values = max_values.compute()
    idxs = np.argmin(np.abs(np.abs(field[:,idz,:])-max_values),axis=0)
    return [idxs,max_values]
    
def get_propaxis(self,field,idx_0 = 0, idx_f=None, idz=None, idx_t=None, find_max = True):
    '''
        Use find_t_max to search the temporal and spatial indices where the field is maximum.
        Return the indices, maximum values and the absolute value of the field along the propagation axis
        at the given temporal index.
        
        If find_max=False, does not perform the search process and idx_t must be provided.
            field: Field name to analyze (elong, ephi, erho, blong, bphi, brho)
            idx_0: Starting point to search along the propagation axis.
            idx_f: Final point to search along the propagation axis.
            idz: Point in the transverse axis to perform the search (distance from the center)
            idx_t: Temporal index to get absolute value of the field along the propagation axis.
            find_max: Flag to enable (True) or disable (False) the max value search process
    '''
    
    nt = self.t.shape[0]
    nz = self.z.shape[0]
    nx = self.x.shape[0]
    
    idz = np.floor(nz/2).astype(np.int32) if idz==None else idz
    idx_max = None
    max_val = None
    if find_max == True:
        idx_max,max_val = self.find_t_max(field=field, idx_0=idx_0, idx_f=idx_f,idz=idz)
        idx_t = idx_max[0]
 
    field = self.select_field[field[0]]["data_cyl"][f"{field}_x3_01"]

    
    data_axis = np.abs(field[idx_t,idz,:])
    
    return [idx_max,max_val,data_axis.compute()]

def get_propaxis_each_x(self,field,idx_0 = 0, idx_f=None, idz=None, idx_t=None, find_max = True):
    '''
        Use find_max_each_x to search the values of maximum field at each position along the propagation axis
        independently of the time.
        
        Return an array with the temporal indices at each point of the propagation axis  and the maximum values the field 
        along the propagation axis at the given temporal index.
        
        If find_max=False, does not perform the search process and idx_t must be provided.
            field: Field name to analyze (elong, ephi, erho, blong, bphi, brho)
            idx_0: Not used
            idx_f: Not used
            idz: Point in the transverse axis to perform the search (distance from the center)
            idx_t: Not used
            find_max: Not used
    '''
    nt = self.t.shape[0]
    nz = self.z.shape[0]
    nx = self.x.shape[0]
    
    idz = np.floor(nz/2).astype(np.int32) if idz==None else idz
    idx_max = None
    max_val = None
    if find_max == True:
        idx_max, max_values = self.find_max_each_x(field=field, idz=idz)
        #idx_t = idx_max[0]
 
    field = self.select_field[field[0]]["data_cyl"][f"{field}_x3_01"]
    
    
    #data_axis = np.abs(field[idx_t,idz,:])
    
    return [idx_max,max_values]

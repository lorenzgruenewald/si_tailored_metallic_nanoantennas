import dask
import dask.array as da
import h5py
import zarr
import os
import glob
from functools import partial
import numpy as np

# File handling module. Our recommendation is not to use directly the hdf5 files for the data processing,
# as they cannot be pickled and can give errors if using multiple workers. Actually, we recommend to perform
# conversion from the hdf5 file to zarr (https://zarr.readthedocs.io/en/stable/) as they allow pickling.
# Once all the data files are converted the all the data processing can be performed using the zarr file format

def __load_single_field_h5(self,path,field_name):
    # Completly read a field, including all the temporal snapshots,
    # into a dask array with dimension 3. The axis=0 is time,
    # and the other two axes are the spatial ones
    [field, dtype, axis, number] = field_name.split('-')
    key = f"{field}_{axis}_{dtype}"
    data = []
    for i in sorted(glob.iglob(f"{path}/{field}-{dtype}/{field_name}*.h5")):
        f = h5py.File(i)
        self._opened_files_h5.append(f)
        data.append(da.from_array(f[key]))
    return da.stack(data,axis=0)
    
def __load_single_field_zarr(self,path,field_name):
    # Load a zarr field. They have the same structured as defined in
    # __load_single_field_h5
    [field, dtype, axis, number] = field_name.split('-')
    key = f"{field}_{axis}_{dtype}"
    return da.from_zarr(f"{path}/zarr/{field}_{axis}_{number}.zarr")

def __load_single_snapshot(self,path,key):
    # Load just a single snapshot from the hdf5 file format
    return da.from_array(h5py.File(path)[key])

def __antenna_lims(self):
    # Function used to calculate the limits of the antenna, from the first zero
    # to the second zero. Maybe in the future might be interesting to check if the
    # measurements of the maximum values are inside or outside the anntena. However,
    # this is not being used.
    
    d_int = dask.delayed(partial(np.sum,axis=0))
    int_antenna = d_int(self.antenna)
    xlims = self.x[np.abs(int_antenna.compute())>0]
    self.antenna_lims = [xlims[0],xlims[-1]]
    
def _create_folder(self,path):
    # Check if the given path exists. If not, create it
    if not os.path.exists(path):
        os.makedirs(path)

def _check_folders(self,path):
    # Check if the paths in the folders exist. If not, create them
    folders = [f"{path}/tmp/",f"{path}/movies/",f"{path}/zarr/efields",
               f"{path}/zarr/bfields",f"{path}/zarr/jfields",
               f"{path}/zarr/electrons",f"{path}/zarr/gold"] 
    for i in folders:
        self._create_folder(i)

def _close_h5_files(self):
    # Close the opened hdf5 files. Usually there is a maximum allowed value of 2048-4096 of opened file descriptors
    [i.close() for i in self._opened_files_h5]

def load_fields_h5(self):
    # Load all the fields using the hdf5 file format. Actually not recommended
    self.storage_method = "h5py"
    self.e_fields = {}
    self.b_fields = {}
    self.j_fields = {}

    for i in self.e_fields_names:
        [field, dtype, axis, number] = i.split('-')
        key = f"{field}_{axis}_{number}"
        self.e_fields[key] = self.conv_e(__load_single_field_h5(self,self.basepath_fields,i),self.w)
    for i in self.b_fields_names:
        [field, dtype, axis, number] = i.split('-')
        key = f"{field}_{axis}_{number}"
        self.b_fields[key] = self.conv_b(__load_single_field_h5(self,self.basepath_fields,i),self.w)
    for i in self.j_fields_names:
        [field, dtype, axis, number] = i.split('-')
        key = f"{field}_{axis}_{number}"
        self.j_fields[key] = __load_single_field_h5(self,self.basepath_fields,i)
    #__antenna_lims(self)
    self._update_dicts()
#        return e_fields, b_fields, j_fields

def convert_h5_to_zarr(self):
    # Method to convert all the files from hdf5 to zarr format.
    # There is a bug. If for any reason, the conversion process fails while executing,
    # and you want to start again, you must delete de zarr folder.
    def __convert_field(field,i):
        data_field = __load_single_field_h5(self,self.basepath_fields,i)
        data_field.to_zarr(f"{self.basepath}/zarr/{field}/{i}.zarr")
        self._close_h5_files()
        
    expected_num_files = np.ceil(self.t.shape[0]/int(self.params["ndump"][0]))
    try:
        a = [__convert_field("efields",i) for i in self.e_fields_names]
        
        if(len(a) != expected_num_files):
            print("Warning!! Less files than expected in efield")
    except zarr.errors.ContainsArrayError:
        print("Path already contains zarr data. ", RuntimeWarning)
        pass
    try:
        a = [__convert_field("bfields",i) for i in self.b_fields_names]
        self._close_h5_files()
        if(len(a) != expected_num_files):
            print("Warning!! Less files than expected in bfield")
    except zarr.errors.ContainsArrayError:
        print("Path already contains zarr data. ", RuntimeWarning)
        pass
    try:
        a = [__convert_field("jfields",i) for i in self.j_fields_names]
        self._close_h5_files()
        if(len(a) != expected_num_files):
            print("Warning!! Less files than expected in jfield")
    except zarr.errors.ContainsArrayError:    
        print("Path already contains zarr data. ", RuntimeWarning)
        pass
    self._close_h5_files()
    

def load_fields_zarr(self):
    # Load all the fields using the hdf5 file format. Actually not recommended
    
    self.storage_method = "zarr"
    self.e_fields = {}
    self.b_fields = {}
    self.j_fields = {}

    #self.antenna = __load_single_snapshot(self,self.antenna_name,"charge_x3_slice")
    for i in self.e_fields_names:
        [field, dtype, axis, number] = i.split('-')
        key = f"{field}_{axis}_{number}"
        self.e_fields[key] = self.conv_e(da.from_zarr(f"{self.basepath}/zarr/efields/{i}.zarr",chunks = "auto"),self.w)
    for i in self.b_fields_names:
        [field, dtype, axis, number] = i.split('-')
        key = f"{field}_{axis}_{number}"
        self.b_fields[key] = self.conv_b(da.from_zarr(f"{self.basepath}/zarr/bfields/{i}.zarr",chunks = "auto"),self.w)
    for i in self.j_fields_names:
        [field, dtype, axis, number] = i.split('-')
        key = f"{field}_{axis}_{number}"
        self.j_fields[key] = da.from_zarr(f"{self.basepath}/zarr/jfields/{i}.zarr",chunks = "auto")
    #__antenna_lims(self)
    self._update_dict()

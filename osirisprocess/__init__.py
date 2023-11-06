import dask
import dask.array as da
import numpy as np
import scipy.constants as const
import imageio as iio
from multiprocessing import Pool 

class OsirisProcess():
    # import all submodules of the object
    from ._dicts_and_lists import _important_dicts_and_lists, _update_dict
    from ._parse_parameters import _parse_runinfo, _grid
    from ._file_handling import load_fields_h5, load_fields_zarr, convert_h5_to_zarr
    from ._file_handling import _check_folders, _close_h5_files, _create_folder
    from .Plugins.convert_to_cyl import convert_to_cyl
    from .Plugins.find_max_values import find_max_values, set_max_values
    from .Plugins.plot import plot
    from .Plugins.process_movies import process_movies
    from .Plugins.get_axis import find_t_max, get_propaxis, find_max_each_x, get_propaxis_each_x
    from .Plugins.integrated_contrast import integrated_contrast
    
    def __init__(self, basepath,nworkers):
        
        self.nworkers = nworkers  # Deprecated. Can be given any value as this is now not used
        self.basepath = basepath  # Path to the simulation folder. This folder must contain at least the run-info file and the MS folder with all the simulation data
        self.basepath_fields = f"{basepath}/MS/FLD/"
        self._opened_files_h5 = []  # List of opened hdf5 files opened to be tracked and eventually to close them 
        self.e_fields = {}  # Dict which will contain the electric field data in cartesian coordinates
        self.b_fields = {}  # Dict which will contain the magnetic field data in cartesian coordinates
        self.j_fields = {}  # Dict which will contain the currents field data in cartesian coordinates
        self.e_fields_cyl = {}  # Dict which will contain the electric field data in cylindrical coordinates
        self.b_fields_cyl = {}  # Dict which will contain the magnetic field data in cylindrical coordinates
        self.j_fields_cyl = {}  # Dict which will contain the currents field data in cylindrical coordinates
        
        # Lambda functions to convert simulation units to SI-derived units
        self.conv_e = lambda x,om_p: x*(om_p*const.m_e*const.c/const.e)/1E9 # GV/m
        self.conv_b = lambda x,om_p: x*om_p*const.m_e/const.e               # T
        self.conv_x = lambda x,om_p: x*const.c/om_p*1E6                     # um 
        self.conv_wl = lambda x,om_p: const.c*2*np.pi/om_p*1E6              # um
        self.conv_t = lambda x,om_p: x/om_p*1E15                            # fs
        
        # Let's convert some lambda functions to delayed dask functions
        self.d_conv_e = dask.delayed(self.conv_e)
        self.d_conv_b = dask.delayed(self.conv_b)
        
        # Only interested in one density snapshot to plot the antenna geometry
        self.antenna_name = f"{basepath}/MS/DENSITY/electrons/charge-slice/charge-slice-electrons-x3-01-000000.h5"
           
        self.params = self._parse_runinfo(basepath)  # Load the simulation data from the run-info file
        self._grid()  # Create the spatial grids
        self._check_folders(basepath)
        self._important_dicts_and_lists()  # Load important dictionaries and lists, containing file names, field names, name conversion tables...
        print("Init finalized")
        
    def __del__(self):
        # Not sure if I'm handling eveything correctly
        for i in list(self.e_fields_cyl.values()): del i
        for i in list(self.b_fields_cyl.values()): del i
        for i in list(self.e_fields.values()): del i
        for i in list(self.b_fields.values()): del i
        for i in list(self.j_fields.values()): del i
        del self.e_fields
        del self.b_fields
        del self.j_fields
        del self.e_fields_cyl
        del self.b_fields_cyl

# si_tailored_metallic_nanoantennas
Supporting files, including input files and analysis scripts for simulations of optical magnetic field enhancement using ultrafast azimuthally polarized laser beams and metallic nanoantennas

Folder antenna_dirs, in each subsubfolder:
- *.3d: template OSIRIS input files
- template_run.sh: template for submit script, adjust to your cluster
- scandata.py: to import, adjust for settings
- Execute template.py to generate a scan
These folders can be used to setup and run OSIRIS simulations.

File si_tailored_metallic_nanoantennas.ipynb:
- Purpose: Loads simulation data from successfully terminated OSIRIS simulations (see input scripts) with the ability to convert the simulation data with the native HDF5 format to the ZARR format, which is better suited for further data analysis with Python.
  It is able to convert the cartesian components of E-fields, B-fields, and charge currents OSIRIS into cylindrical components of each simulation.
  It is able to find the global maximum E-field and B-field maxima of each simulation.
  It is able to save the global E-field/B-field maxima in a pickle file (https://docs.python.org/3/library/pickle.html).
  Processing of data is parallelized up to an arbitrary number of parallely working DASK clients.
- Requirements & Recommendations:

  --> Successful termination of all simulations within a scan (see input files)
  
  --> Conda environment with installed packages according to packages_conda.txt
  
- Call as: Jupyter notebook 
- Output:

  --> */SCAN/SCAN0*/tmp/*png: Plots of different cylindrical field components for different analysis slices (defined in the OSIRIS input script) for each saved timestep in the simulation.
  
  --> */SCAN/SCAN0*/zarr: Contains the simulation data in ZARR format
  
  --> */SCAN/SCAN0*/movies/*gif: Contains the movies of different cylindrical field components for different analysis slices (defined in the OSIRIS input script) covering the saved timesteps in the simulation.
  
Folder osirisprocess:
- imported by si_tailored_metallic_nanoantennas.ipynb

IMPORTANT: 
There is a small bug in the code of OSIRIS (dev branch, v4.4.4) not handling correctly the LG beam case with charge -1. If you construct the APB from LG modes (we use HG modes in the inputs), this needs to be fixed. You have to modify the file source/zpulse/os-zpulse-std.f03 in line 2903:

The original line:
    ( sqrt(rho2)*sqrt(rWl2)/this%per_w0(1) )**this%per_tem_mode(2) * &
    
The modified line:
    ( sqrt(rho2)*sqrt(rWl2)/this%per_w0(1) )**abs(this%per_tem_mode(2)) * &

(vortex charge should be absolute in the exponent)

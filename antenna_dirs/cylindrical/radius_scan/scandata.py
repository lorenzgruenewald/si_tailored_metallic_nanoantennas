import numpy as np

# Dictionary with the parameters to substitute inside template_ring.3d file
parameters = {"frequency": "3.57092270562937d15",
              "nodelist": "3,4,4",
              "dt": "0.02",
              "ndump": "30",
              "ndump_mat": "179",
              "xmin": "0.0",
              "xmax": "29.778129",
              "ymin": "-77.4231365",
              "ymax": "77.4231365",
              "zmin": "-77.4231365",
              "zmax": "77.4231365",
              "tmax": "107.127104",
              "antenna_density": "34.5",
              "antenna_xmin": "10.06",  
              "antenna_xmax": "15.06", 
              "antenna_L": "3.768",
              "antenna_r0": "21.11",
              "beam_a0": "0.0001642943346196797",
              "beam_trise": "17.85451722567634",
              "beam_tfall": "17.85451722567634",
              "beam_w0": "29.77812941791273",
              "beam_focus": "14.88990645"}

# Define antenna density in simulation units


def n_au(wp): 
    return (5.9E22)/(wp**2*3.14201193E-10)


parameters["antenna_density"] = str(n_au(float(parameters["frequency"].replace("d", "E"))))

njobs=1 # Number of jobs per batch file to run
# Range of values to scan
datascan = np.around(np.arange(6.0, 40.0, 1.0),2).astype('str')
# Which is the variable from the dictionary above I want to iterate
keyscan = "antenna_r0"
# Common folder name
basename = "RingAntenna_l3.768_r"

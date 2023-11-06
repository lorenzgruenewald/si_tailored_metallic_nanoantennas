import numpy as np

parameters = {"frequency": "3.57092270562937d15",
              "nodelist": "4,4,4",
              "dt": "0.02",
              "ndump": "30",
              "ndump_fac": "100",     
              "xmin": "0.0",
              "xmax": "59.5565800662899",
              "ymin": "-77.4231365",
              "ymax": "77.4231365",
              "zmin": "-77.4231365",
              "zmax": "77.4231365",
              "tmax": "107.127104",
              "antenna_density": "34.5",
              "antenna_L": "3.768",
              "antenna_rmax": "21.11",
              "antenna_rmin": "14.29",
              "gauss_width": "0.0",
              "gauss_amplitude": "0.0",
              "gauss_offset": "0.0",
              "beam_a0": "0.0001642943346196797",
              "beam_trise": "17.85451722567634",
              "beam_tfall": "17.85451722567634",
              "beam_w0": "29.77812941791273",
              "beam_focus": "29.77829003314495"}

#Setting parameters antenna_xmin, antenna_xmax for parabola
def n_au(wp): return (5.9E22)/(wp**2*3.14201193E-10)
parameters["antenna_density"] = str(n_au(float(parameters["frequency"].replace("d","E"))))

#datascan = np.around(np.arange(0.0, 10.0, 0.2),2).astype('str')
njobs = 1
datascan = (np.arange(0.5,24.0,0.5)).astype("str") 

#lengths = np.arange(0.05*2*np.pi, 2*2.0*np.pi,0.05*6.28)
#datascan = np.round(lengths,3).astype(str)
keyscan = "antenna_L"
basename = "length21.11"

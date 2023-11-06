import numpy as np

parameters = {"frequency": "3.57092270562937d15",
              "nodelist": "4,4,4",
              "dt": "0.02",
              "ndump_mat": "179", 
              "ndump": "20",
              "xmin": "0.0",
              "xmax": "29.778129",
              "ymin": "-77.4231365",
              "ymax": "77.4231365",
              "zmin": "-77.4231365",
              "zmax": "77.4231365",
              "tmax": "53.563552",
              "antenna_density": "34.5",
              "antenna_xmin": "10.06",
              "antenna_xmax": "15.06",
              "antenna_L": "5.0",
              "antenna_r0": "21.11",
              "beam_a0": "0.0001642943346196797",
              "beam_trise": "17.85451722567634",
              "beam_tfall": "17.85451722567634",
              "beam_w0": "29.77812941791273",
              "beam_focus": "14.88990645"}


def n_au(wp): 
    return (5.9E22)/(wp**2*3.14201193E-10)


parameters["antenna_density"] = str(n_au(float(parameters["frequency"].replace("d", "E"))))

njobs = 1
lengths = np.arange(0.05*2*np.pi, 2*2.0*np.pi, 0.05*6.28)
datascan = np.round(lengths, 3).astype(str)
keyscan = "antenna_L"
basename = "RingAntenna_r21.11_l"

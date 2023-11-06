import re
import numpy as np
from functools import partial

def _parse_runinfo(self,path):
    # Parse the run-info file and extract the simulation parameters.
    # These parameters are stored in a dictionary as strings.
    with open(f"{path}/run-info",'r') as f:
        a = f.readlines()
    patterns = ["(omega_p0)", "(nx_p)","(xmin)","(xmax)","(dt)","(tmax)","(ndump)"]
    regex = list(map(re.compile,patterns))
    params = [list(map(partial(re.sub,*["(\t|\n|,|!.+(?=\s)|\s|(\(1:3\)))",""]),k)) for k in list(map(partial(re.split,", | ="),[list(filter(i.search, a))[0] for i in regex]))]
    params = [i if not 'tmax' in i else i[2:] for i in params]
    params_d = {params[i][0]: params[i][1:] for i in range(len(params))}
    return params_d

def _grid(self):
    # Define the spatio-temporal grid based on the simulation parameters and convert to human units.
    self.w = float(self.params["omega_p0"][0].replace("d","E"))
    self.x = self.conv_x(np.linspace(float(self.params["xmin"][0]),float(self.params["xmax"][0]),int(self.params["nx_p"][0])),self.w)
    self.y = self.conv_x(np.linspace(float(self.params["xmin"][1]),float(self.params["xmax"][1]),int(self.params["nx_p"][1])),self.w)
    self.z = self.conv_x(np.linspace(float(self.params["xmin"][2]),float(self.params["xmax"][2]),int(self.params["nx_p"][2])),self.w)
    self.dx = (self.x[-1]-self.x[0])/(self.x.shape[0])
    self.dy = (self.y[-1]-self.y[0])/(self.y.shape[0])
    self.dz = (self.z[-1]-self.z[0])/(self.z.shape[0])
    self.dt = self.conv_t(float(self.params["dt"][0]),self.w)
    self.t = np.arange(0.0, self.conv_t(float(self.params["tmax"][0]),self.w),self.dt*int(self.params["ndump"][0]))
    Y,Z = np.meshgrid(self.y,self.z)
    self.Phi = np.mod(np.arctan2(Z,Y),2*np.pi)

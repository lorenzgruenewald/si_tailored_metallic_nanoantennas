import dask.array as da
import numpy as np

# Convert from cartesian data to cylindrical data

def convert_to_cyl(self):
    sin_phi = np.sin(self.Phi)
    cos_phi = np.cos(self.Phi)
    d_sin_phi = da.from_array(np.sin(self.Phi))
    d_cos_phi = da.from_array(np.cos(self.Phi))
    
    # Conversion functions if the slice is along x1
    long_x1 = lambda f1,f2,f3:  f1
    rho_x1  = lambda f1,f2,f3:  f2*d_cos_phi + f3*d_sin_phi
    phi_x1  = lambda f1,f2,f3: -f2*d_sin_phi + f3*d_cos_phi
    
    # Conversion functions if the slice is along x2. Phi = 0
    long_x2 = lambda f1,f2,f3:  f1
    rho_x2  = lambda f1,f2,f3:  f3
    phi_x2  = lambda f1,f2,f3:  f2

    # Conversion functions if the slice is along x3. Phi = pi/2
    long_x3 = lambda f1,f2,f3:  f1
    rho_x3  = lambda f1,f2,f3:  f2
    phi_x3  = lambda f1,f2,f3:  f3

    # Dict to relate from the axis names to the actual conversion functions
    conv_funcs_d = {"x1": [long_x1, rho_x1, phi_x1],
                    "x2": [long_x2, rho_x2, phi_x2],
                    "x3": [long_x3, rho_x3, phi_x3]}

    efield_to_num = {"elong":0, "erho":1, "ephi":2}
    bfield_to_num = {"blong":0, "brho":1, "bphi":2}

    self.e_fields_cyl = {}
    self.b_fields_cyl = {}
    
    # Perform the conversion from cartesian to cylindrical 
    for i in self.e_fields_names_cyl:
        [field, axis, number] = i.split('-')
        key = i.replace('-','_')
        key2 = f"{axis}_{number}"
        self.e_fields_cyl[key] = conv_funcs_d[axis][efield_to_num[field]](self.e_fields[f"e1_{key2}"],self.e_fields[f"e2_{key2}"],self.e_fields[f"e3_{key2}"])

    for i in self.b_fields_names_cyl:
        [field, axis, number] = i.split('-')
        key = i.replace('-','_')
        key2 = f"{axis}_{number}"
        self.b_fields_cyl[key] = conv_funcs_d[axis][bfield_to_num[field]](self.b_fields[f"b1_{key2}"],self.b_fields[f"b2_{key2}"],self.b_fields[f"b3_{key2}"])
    self._update_dict()
# Here we define some dictionaries and list which are going to be used several times inside the object.
# This dictionaries allow us to much some names or identifiers with other strings. 
# For example, in self.select_field, if we access with the key "e", then this will give us another dict
# containing the title (Electric field), which is title for colobar when plotting, the axis title, 
# the list containing the field names and the data in both cartesian and cylindrical coordinates.

def _important_dicts_and_lists(self):
        # List containing the field data slices names given by Osiris for the e-field, b-field and currents j
        self.e_fields_names = ["e1-slice-x1-01","e1-slice-x1-02","e1-slice-x2-01","e1-slice-x3-01",
                               "e2-slice-x1-01","e2-slice-x1-02","e2-slice-x2-01","e2-slice-x3-01",
                               "e3-slice-x1-01","e3-slice-x1-02","e3-slice-x2-01","e3-slice-x3-01",]

        self.b_fields_names = ["b1-slice-x1-01","b1-slice-x1-02","b1-slice-x2-01","b1-slice-x3-01",
                               "b2-slice-x1-01","b2-slice-x1-02","b2-slice-x2-01","b2-slice-x3-01",
                               "b3-slice-x1-01","b3-slice-x1-02","b3-slice-x2-01","b3-slice-x3-01",]

        self.j_fields_names = ["j1-slice-x3-01",
                               "j2-slice-x3-01",
                               "j3-slice-x3-01"]
    
        # List of names I define once the fields are converted to cylindrical coordinates
        self.e_fields_names_cyl = ["elong-x1-01","elong-x1-02","elong-x2-01","elong-x3-01",
                                   "erho-x1-01","erho-x1-02","erho-x2-01","erho-x3-01",
                                   "ephi-x1-01","ephi-x1-02","ephi-x2-01","ephi-x3-01",]

        self.b_fields_names_cyl = ["blong-x1-01","blong-x1-02","blong-x2-01","blong-x3-01",
                                   "brho-x1-01","brho-x1-02","brho-x2-01","brho-x3-01",
                                   "bphi-x1-01","bphi-x1-02","bphi-x2-01","bphi-x3-01",]
        
        # Dictionary containing essential data for each field
        self.select_field = {"e": {"title": "Electric field",
                                  "cbar_title": "Electric field (GV/m)",
                                  "ax_title": "E",
                                  "field_names": self.e_fields_names_cyl,
                                  "data_cart": self.e_fields,
                                  "data_cyl": self.e_fields_cyl,
                                  "axis": ["x1","x2","x3"],
                                  "slices": {"x1": ["01","02",],"x2": ["01"],"x3": ["01"]}},
                            "b": {"title": "Magnetic field",
                                  "cbar_title": "Magnetic field (T)",
                                  "ax_title": "B",
                                  "field_names": self.b_fields_names_cyl,
                                  "data_cart": self.b_fields,
                                  "data_cyl": self.b_fields_cyl,
                                  "axis": ["x1","x2","x3"],
                                  "slices": {"x1": ["01","02",],"x2": ["01"],"x3": ["01"]}},
                            "j": {"title": "Currents",
                                  "cbar_title": "Currents",
                                  "ax_title": "J",
                                  "field_names": self.j_fields_names,
                                  "data_cart": self.j_fields,
                                  "data_cyl": self.j_fields_cyl,
                                  "axis": ["x3"],
                                  "slices": {"x1": ["01","02",],"x2": ["01"],"x3": ["01"]}}}
        
        # Dictionary to select the parameters of the axis and the max-min values for the grid/plotting
        self.select_axis = {"x1": {"x": "y (um)",
                              "y": "z (um)",
                              "xmin": self.y[0],
                              "xmax": self.y[-1],
                              "ymin": self.z[0],
                              "ymax": self.z[-1]},
                       "x2": {"x": "x (um)",
                              "y": "z (um)",
                              "xmin": self.x[0],
                              "xmax": self.x[-1],
                              "ymin": self.z[0],
                              "ymax": self.z[-1]},
                       "x3": {"x": "x (um)",
                              "y": "y (um)",
                              "xmin": self.x[0],
                              "xmax": self.x[-1],
                              "ymin": self.y[0],
                              "ymax": self.y[-1]}}
        
        # Dictionary that we define to match to each field in the keys a list of
        # which are positions in field data where we search for the maximum value.
        # E.g.: for "elong_x1_01" we want the maximum electric field values globally and at the center 
        # of the slice. On the other hand got "ephi_x3_01", we search for the maximum values globally,
        # at the center of the slice, at 50% of the x2 axis (our propagation axis actually), at 60%, 
        # at 70%... This rules are defined inside Plugins/find_max_values.py
        
        self.rules_max_values = {"elong_x1_01": ["global","center"],
                                   "elong_x1_02": ["global","center"],
                                   "erho_x1_01":  ["global","center"],
                                   "erho_x1_02":  ["global","center"],
                                   "ephi_x1_01":  ["global","center"],
                                   "ephi_x1_02":  ["global","center"],
                                   "elong_x2_01": ["global","center","global_axis_x2","half_to_end_x2",
                                                   "50_axis_x2","60_axis_x2","70_axis_x2","80_axis_x2","90_axis_x2"],
                                   "erho_x2_01":  ["global","center","global_axis_x2","half_to_end_x2",
                                                   "50_axis_x2","60_axis_x2","70_axis_x2","80_axis_x2","90_axis_x2"],
                                   "ephi_x2_01":  ["global","center","global_axis_x2","half_to_end_x2",
                                                   "50_axis_x2","60_axis_x2","70_axis_x2","80_axis_x2","90_axis_x2"],
                                   "elong_x3_01": ["global","center","global_axis_x2","half_to_end_x2",
                                                   "50_axis_x2","60_axis_x2","70_axis_x2","80_axis_x2","90_axis_x2"],
                                   "erho_x3_01":  ["global","center","global_axis_x2","half_to_end_x2",
                                                   "50_axis_x2","60_axis_x2","70_axis_x2","80_axis_x2","90_axis_x2"],
                                   "ephi_x3_01":  ["global","center","global_axis_x2","half_to_end_x2",
                                                   "50_axis_x2","60_axis_x2","70_axis_x2","80_axis_x2","90_axis_x2"],
                                   "blong_x1_01": ["global","center"],
                                   "blong_x1_02": ["global","center"],
                                   "brho_x1_01":  ["global","center"],
                                   "brho_x1_02":  ["global","center"],
                                   "bphi_x1_01":  ["global","center"],
                                   "bphi_x1_02":  ["global","center"],
                                   "blong_x2_01": ["global","center","global_axis_x2","half_to_end_x2",
                                                   "50_axis_x2","60_axis_x2","70_axis_x2","80_axis_x2","90_axis_x2"],
                                   "brho_x2_01":  ["global","center","global_axis_x2","half_to_end_x2",
                                                   "50_axis_x2","60_axis_x2","70_axis_x2","80_axis_x2","90_axis_x2"],
                                   "bphi_x2_01":  ["global","center","global_axis_x2","half_to_end_x2",
                                                   "50_axis_x2","60_axis_x2","70_axis_x2","80_axis_x2","90_axis_x2"],
                                   "blong_x3_01": ["global","center","global_axis_x2","half_to_end_x2",
                                                   "50_axis_x2","60_axis_x2","70_axis_x2","80_axis_x2","90_axis_x2"],
                                   "brho_x3_01":  ["global","center","global_axis_x2","half_to_end_x2",
                                                   "50_axis_x2","60_axis_x2","70_axis_x2","80_axis_x2","90_axis_x2"],
                                   "bphi_x3_01":  ["global","center","global_axis_x2","half_to_end_x2",
                                                   "50_axis_x2","60_axis_x2","70_axis_x2","80_axis_x2","90_axis_x2"]}

def _update_dict(self):
    # List of files that have to be updated if they are changed.
    self.select_field["e"]["data_cart"] = self.e_fields
    self.select_field["e"]["data_cyl"]  = self.e_fields_cyl
    self.select_field["b"]["data_cart"] = self.b_fields
    self.select_field["b"]["data_cyl"]  = self.b_fields_cyl
    self.select_field["j"]["data_cart"] = self.j_fields
    self.select_field["j"]["data_cyl"]  = self.j_fields_cyl

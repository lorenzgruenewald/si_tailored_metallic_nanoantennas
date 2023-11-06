import numpy as np
import dask.array as da
import dask

def __parse_rule(self, rule):
    # Dict to map the axis names x1,..x3 to the number of points in simulation box obtained from the run-info
    rule_map_axis={"x1": (int(self.params["nx_p"][1]),int(self.params["nx_p"][2])),
                   "x2": (int(self.params["nx_p"][1]),int(self.params["nx_p"][0])),
                   "x3": (int(self.params["nx_p"][2]),int(self.params["nx_p"][0]))}
   
    # Rules definition to search for the maximum values. We define for each name a lambda function
    # which takes two parameters, the number of points for each spatial axis.
    # The lambda functions return the slices to define the constraints of the search.
    # IMPORTANT: the names x1, x2 does not refer to the osiris axis. Here, they refere to the first and second axis of the data slice.
    rule_map_region={"global": lambda nx, ny: (slice(0,nx), slice(0,ny)), # Maximum value globally
                     "center": lambda nx, ny: (slice(int(nx/2),int(nx/2)+1), slice(int(ny/2),int(ny/2)+1)), #Maximum value at the center of the data slice
                     "global_axis_x1": lambda nx,ny: (slice(int(nx/2),int(nx/2)+1), slice(0,ny)), # Maximum value along the first axis (x2 = 0)
                     "global_axis_x2": lambda nx,ny: (slice(0,nx), slice(int(ny/2),int(ny/2)+1)), # Maximum value along the second axis (x1 = 0)
                     "half_to_end_x1": lambda nx,ny: (slice(int(nx/2), int(nx/2)+1), slice(0,ny)), # Maximum value inside the second half of the simulation box (for x1 axis)
                     "half_to_end_x2": lambda nx,ny: (slice(0,nx), slice(int(ny/2),int(ny/2)+1)), # Maximum value inside the second half of the simulation box (for x2 axis)
                     "50_axis_x1": lambda nx,ny: (slice(int(nx*5/10),int(nx*5/10)+1), slice(int(ny/2), int(ny/2)+1)),  # Maximum value at x1 = 50% and x2 = 0
                     "60_axis_x1": lambda nx,ny: (slice(int(nx*6/10),int(nx*6/10)+1), slice(int(ny/2), int(ny/2)+1)),  # Maximum value at x1 = 60% and x2 = 0
                     "70_axis_x1": lambda nx,ny: (slice(int(nx*7/10),int(nx*7/10)+1), slice(int(ny/2), int(ny/2)+1)),  # Maximum value at x1 = 70% and x2 = 0
                     "80_axis_x1": lambda nx,ny: (slice(int(nx*8/10),int(nx*8/10)+1), slice(int(ny/2), int(ny/2)+1)),  # Maximum value at x1 = 80% and x2 = 0
                     "90_axis_x1": lambda nx,ny: (slice(int(nx*9/10),int(nx*9/10)+1), slice(int(ny/2), int(ny/2)+1)),  # Maximum value at x1 = 90% and x2 = 0
                     "50_axis_x2": lambda nx,ny: (slice(int(nx/2),int(nx/2)+1), slice(int(ny*5/10), int(ny*5/10)+1)),  # Maximum value at x1 = 0 and x2 = 50%
                     "60_axis_x2": lambda nx,ny: (slice(int(nx/2),int(nx/2)+1), slice(int(ny*6/10), int(ny*6/10)+1)),  # Maximum value at x1 = 0 and x2 = 60%
                     "70_axis_x2": lambda nx,ny: (slice(int(nx/2),int(nx/2)+1), slice(int(ny*7/10), int(ny*7/10)+1)),  # Maximum value at x1 = 0 and x2 = 70%
                     "80_axis_x2": lambda nx,ny: (slice(int(nx/2),int(nx/2)+1), slice(int(ny*8/10), int(ny*8/10)+1)),  # Maximum value at x1 = 0 and x2 = 80%
                     "90_axis_x2": lambda nx,ny: (slice(int(nx/2),int(nx/2)+1), slice(int(ny*9/10), int(ny*9/10)+1)),} # Maximum value at x1 = 0 and x2 = 90%
    axis,region = rule.split('-')
    return rule_map_region[region](*rule_map_axis[axis])

def __make_rule(self,dict_values):
    return {i: ['-'.join([i.split('_')[1],j]) for j in dict_values[i]] for i in dict_values.keys()}

def set_max_values(self,max_values_dict):
    # Method to set a dict of maximum values inseted of recalculating them again
    self.max_values = max_values_dict

def find_max_values(self):
    # Search for the maximum values given the rules in _dicts_and_lists.py
    d_abs = dask.delayed(np.abs)
    d_max = dask.delayed(np.max)

    rules = __make_rule(self,self.rules_max_values)
    operations = []
    for i in rules.keys():
        field_to_analyze = self.select_field[i[0]]["data_cyl"]
        for j in rules[i]:
            rule = __parse_rule(self,j)
            op1 = d_abs(field_to_analyze[i][:,rule[0],rule[1]]) 
            op2 = d_max(op1)
            operations.append(op2)
    result = list(dask.compute(*operations,num_workers=self.nworkers))

    self.max_values = {self.basepath:{}}
    for i in rules.keys():
        self.max_values[self.basepath].update({i: {}})
        for j in rules[i]:
            self.max_values[self.basepath][i].update({j.split('-')[1]: result.pop(0)})         
    return self.max_values
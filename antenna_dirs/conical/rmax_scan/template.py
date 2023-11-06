import os
import numpy as np
from string import Template
from scandata import parameters, datascan, keyscan, basename, njobs

def gendecks(data, key, name):
    paths = []
    with open('template_conical.3d', 'r') as f:
        src = Template(f.read())

        for i in data:
            parameters[key] = i
            parameters["antenna_xmin"] = str((float(parameters["xmax"]) - float(parameters["xmin"]))/2.0 - float(parameters["antenna_L"])/2.0)          
            parameters["antenna_xmax"] = str((float(parameters["xmax"]) - float(parameters["xmin"]))/2.0 + float(parameters["antenna_L"])/2.0)   
            result = src.substitute(parameters)
            foldername = f"{name}{i}"
            if not os.path.exists(foldername):
                os.makedirs(foldername)
            paths.append(foldername)
            with open(f'{foldername}/simulation.3d', 'w') as fo:
                fo.write(result)

            print(i)

    nfiles = int(len(paths)/njobs) + 1
    print(paths)
    path_arr = " ".join([elem for elem in paths])
    jobname_arr = " ".join([str(el.split("_")[-3]) for el in paths])
    listjobs = f"mpirun -n $SLURM_TASKS_PER_NODE OSIRIS_PATH/osiris-3D.e simulation.3d > $SLURM_SUBMIT_DIR/${{file_arr[$SLURM_ARRAY_TASK_ID]}}/osiris.log"
   
    batch = {"name": f"ConicalScan",
            "nodenumber": f"{njobs}",
            "ntasks": "48",
            "filenumber": f"{nfiles}",
            "path_arr": f"({path_arr})",
            "jobnames": f"{listjobs}",
            }
    with open("template_run.sh", "r") as f:
            src = Template(f.read())
            result = src.substitute(batch)
            with open(f"run_array.sh", "w") as fo:
                fo.write(result)

gendecks(datascan, keyscan, basename)

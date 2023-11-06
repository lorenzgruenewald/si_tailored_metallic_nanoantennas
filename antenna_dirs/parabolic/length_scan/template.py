import os
import numpy as np
from string import Template
from scandata import parameters, datascan, keyscan, basename, njobs

def gendecks(data, key, name):
    paths = []
    with open('template_parabola.3d', 'r') as f:
        src = Template(f.read())

        for i in data:
            parameters[key] = i
            parameters["antenna_focal_length"] = str(complex((complex(parameters["antenna_rmin"])**2-complex(parameters["antenna_rmax"])**2)/(4*complex(parameters["antenna_L"]))).real)
            parameters["parabola_base_point"] = str(complex((complex(parameters["xmax"])-complex(parameters["xmin"])-complex(parameters["antenna_L"]))*(0.5)-(complex(parameters["antenna_rmax"]).real)**2/(4*complex(parameters["antenna_focal_length"])).real).real)
            parameters["antenna_xmin"] = str(complex(-complex(parameters["antenna_L"])*(complex(parameters["antenna_rmax"])**2)/(complex(parameters["antenna_rmax"])**2-complex(parameters["antenna_rmin"])**2)+complex(parameters["parabola_base_point"])).real)
            parameters["antenna_xmax"] = str(complex(-complex(parameters["antenna_L"])*(complex(parameters["antenna_rmin"])**2)/(complex(parameters["antenna_rmax"])**2-complex(parameters["antenna_rmin"])**2)+complex(parameters["parabola_base_point"])).real)
            result = src.substitute(parameters)
            foldername = f"{name}_real_{round(complex(i).real,2)}_imag_{round(complex(i).imag,2)}"
            print(f'Antenna focal length: {parameters["antenna_focal_length"]}')
            print(f'Antenna focal length in nm: {float(parameters["antenna_focal_length"])*83.95377965683578}')
            print(f'Parabola base point: {(parameters["parabola_base_point"])}')  
            print(f'Antenna xmin: {(parameters["antenna_xmin"])}')
            print(f'Antenna xmax: {(parameters["antenna_xmax"])}')
            print(f'rmin: {(parameters["antenna_rmin"])} ')
            print(f'Antenna length: {parameters["antenna_L"]} ')
           
           
            if (parameters["antenna_xmax"]) >= (parameters["xmax"]):
                print("antenna_xmax exceeds box")
            if (parameters["antenna_xmin"]) <= (parameters["xmin"]):
                print("antenna_xmin exceeds box")
            if not os.path.exists(foldername):
                os.makedirs(foldername)
            paths.append(foldername)
            with open(f'{foldername}/simulation.3d', 'w') as fo:
                fo.write(result)

            

    nfiles = int(len(paths)/njobs) 
	
    for k in range(nfiles):
        listjobs = []

        for i in paths[k*njobs:(k+1)*njobs]:
            listjobs.append(
                f"mpirun -n $SLURM_TASKS_PER_NODE /scratch/manganese/oppel/osiris-dev/bin/osiris-3D.e simulation.3d > $SLURM_SUBMIT_DIR/{i}/osiris.log"
)
        batch = {"name": f"Parabola_rmin_Scan_{k}",
                 "nodenumber": f"{njobs}",
                 "ntasks": "64",
                 "jobnames": "\n".join(listjobs),
                 "foldername": f"{paths[k]}"}

        with open("template_run.sh", "r") as f:
            src = Template(f.read())
            result = src.substitute(batch)
            with open(f"run_rmin_scan_{k}.sh", "w") as fo:
                fo.write(result)

print(datascan, keyscan, basename)
gendecks(datascan, keyscan, basename)



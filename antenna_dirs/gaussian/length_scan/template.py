import os
import numpy as np
from string import Template
from scandata import parameters, datascan, keyscan, basename, njobs

def gendecks(data, key, name):
    paths = []
    with open('template_gauss.3d', 'r') as f:
        src = Template(f.read())

        for i in data:
            parameters[key] = i
            parameters["antenna_focal_length"] = str(complex((complex(parameters["antenna_rmin"])**2-complex(parameters["antenna_rmax"])**2)/(4*complex(parameters["antenna_L"]))).real)
            parameters["parabola_base_point"] = str(complex((complex(parameters["xmax"])-complex(parameters["xmin"])-complex(parameters["antenna_L"]))*(0.5)-(complex(parameters["antenna_rmax"]).real)**2/(4*complex(parameters["antenna_focal_length"])).real).real)
            parameters["antenna_xmin"] = str(complex(-complex(parameters["antenna_L"])*(complex(parameters["antenna_rmax"])**2)/(complex(parameters["antenna_rmax"])**2-complex(parameters["antenna_rmin"])**2)+complex(parameters["parabola_base_point"])).real)
            parameters["antenna_xmax"] = str(complex(-complex(parameters["antenna_L"])*(complex(parameters["antenna_rmin"])**2)/(complex(parameters["antenna_rmax"])**2-complex(parameters["antenna_rmin"])**2)+complex(parameters["parabola_base_point"])).real)


            # Gauss definitions
            parameters["gauss_amplitude"] = str(float(parameters["antenna_rmax"])**2/(-4*float(parameters["antenna_focal_length"])))
            parameters["gauss_width"] = str(float(parameters["antenna_rmax"])/np.sqrt(2))
            parameters["gauss_base_point"] = str(complex((complex(parameters["xmax"])-complex(parameters["xmin"])-complex(parameters["antenna_L"]))*(0.5)).real)


            print("Parabola:")
            print(f'Antenna focal length : {float(parameters["antenna_focal_length"])}')#*83.95377965683578}')
            print(f'Parabola base point: {(parameters["parabola_base_point"])}')
            print(f'Antenna xmin: {(parameters["antenna_xmin"])}')
            print(f'Antenna xmax: {(parameters["antenna_xmax"])}')
            print(f'rmin: {(parameters["antenna_rmin"])} ')
            print(f'rmax: {(parameters["antenna_rmax"])} ')
            print(f'Antenna length: {parameters["antenna_L"]} \n')
            print("Gaussian:")
            print(f'Gaussian amplitude: {(parameters["gauss_amplitude"])} ')
            print(f'Gaussian width: {(parameters["gauss_width"])} ')
            print(f'Gaussian offset: {(parameters["gauss_offset"])} ')
            print("------------------------------")

            result = src.substitute(parameters)
            foldername = f"{name}_{np.round(complex(i).real,2)}"
            if not os.path.exists(foldername):
                os.makedirs(foldername)
            paths.append(foldername)
            with open(f'{foldername}/simulation.3d', 'w') as fo:
                fo.write(result)


    nfiles = int(len(paths)/njobs) + 1
    print(paths)
    path_arr = " ".join([elem for elem in paths])
    jobname_arr = " ".join([str(el.split("_")[-2]) for el in paths])
    listjobs = f"mpirun -n $SLURM_TASKS_PER_NODE /scratch/manganese/oppel/osiris-dev/bin/osiris-3D.e simulation.3d > $SLURM_SUBMIT_DIR/${{file_arr[$SLURM_ARRAY_TASK_ID]}}/osiris.log"

    batch = {"name": f"GaussScan_dl",
            "nodenumber": f"{njobs}",
            "ntasks": "64",
            "filenumber": f"{nfiles}",
            "path_arr": f"({path_arr})",
            "jobnames": f"{listjobs}",
            }
    with open("template_run.sh", "r") as f:
            src = Template(f.read())
            result = src.substitute(batch)
            with open(f"run_array.sh", "w") as fo:
                fo.write(result)


print(datascan, keyscan, basename)
gendecks(datascan, keyscan, basename)


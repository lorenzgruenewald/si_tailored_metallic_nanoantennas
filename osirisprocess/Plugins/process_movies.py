import dask
import imageio as iio
import glob

def process_movies(self):
    # Convert all the plots into an animated gid
    image_paths = f"{self.basepath}/tmp/"
    movies_path = f"{self.basepath}/movies/"
    movies_names = [i.replace(image_paths,"") for i in glob.iglob(f"{image_paths}/*")]
    def __process(movies_path,image_paths,movie_name):
        with iio.get_writer(f"{movies_path}/{movie_name}.gif") as writer:
            for filename in sorted(glob.iglob(f"{image_paths}/{movie_name}/*.png")):
                image = iio.imread(filename)
                writer.append_data(image)
    
    # Delayed __process so can be executed in parallel
    d_process = dask.delayed(__process)
    ops = []
    for i in movies_names:
        ops.append(d_process(movies_path, image_paths, i))
    dask.compute(*ops,num_workers=self.nworkers)
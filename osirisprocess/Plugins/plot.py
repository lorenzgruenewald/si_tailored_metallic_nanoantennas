import copy
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import dask
from cmcrameri import cm

def plot(self):
    # Method to perform the plots
    d_abs = dask.delayed(np.abs)
    __select_fields = copy.deepcopy(self.select_field)
    __select_fields["e"].pop("data_cart")
    __select_fields["e"].pop("data_cyl")
    __select_fields["b"].pop("data_cart")
    __select_fields["b"].pop("data_cyl")
    __select_fields["j"].pop("data_cart")
    __select_fields["j"].pop("data_cyl")
    
    # Iterate over all the fields (e,b,j), axis (x1, x2, x3) and slices (if there is more than one. For example, for x1 we have slices 01 and 02)
    for i in self.select_field.keys():
        for axs in self.select_field[i]["axis"]:
            for slc in self.select_field[i]["slices"][axs]:
                
                kind = i
                axis = axs
                data_slice = slc

                filenames = []
                datanames = [i.replace('-','_').replace('slice_','')  for i in filter(lambda x:axis in x and data_slice in x,self.select_field[kind]["field_names"])]
                print(datanames)
                
                # Plot function, takes lots of arguments, like a list with the field data, the kind, axis and slice, the name, ouputpath, maximum values, the time array...
                def __plot(field_list,kind,axis,slc,datanames,path,sfield,saxis,maxf,t,ti):
                    # import matplotlib.pyplot as plt
                    # import matplotlib
                    from cmcrameri import cm
                    plt.rcParams['image.cmap'] = 'cmc.batlowW_r' 
                    matplotlib.use('Agg')
                    #plt.rcParams.update({
                    #                    "text.usetex": True,
                    #                    "font.family": "Helvetica"
                    #                    })
                    title = sfield[kind]["title"]
                    x_label = saxis[axis]["x"]
                    y_label = saxis[axis]["y"]
                    cbar_title = sfield[kind]["cbar_title"]
                    ax_title_name = sfield[kind]["ax_title"]
        #
                    min_f = 0.0
                    max_f = maxf
                    xmin = saxis[axis]["xmin"]
                    xmax = saxis[axis]["xmax"]
                    ymin = saxis[axis]["ymin"]
                    ymax = saxis[axis]["ymax"]
                    ticksize = 20
                    titlesize = 40
                    axistitlesize = 25
                    axislabelsize = 20

                    field_long = field_list[0]
                    field_rho = field_list[1]
                    field_phi = field_list[2]

                    fig = plt.figure(figsize=(18,8))
                    gs = fig.add_gridspec(2,4,width_ratios=[1,1,1,0.05],height_ratios=[0.1,1])
                    ax_title = fig.add_subplot(gs[0,:-1])
                    ax_long = fig.add_subplot(gs[1,0])
                    ax_rho = fig.add_subplot(gs[1,1])
                    ax_phi = fig.add_subplot(gs[1,2])
                    ax_bar = fig.add_subplot(gs[1,3])
        #
                    ax_title.axis('off')
                    ax_title.text(0.5,0.5,title, ha='center',va='center',fontsize=titlesize,fontweight='bold')
                    ax_title.text(0.85,0.1,f"t = {str(round(t,3))} fs",va="bottom", fontsize=axistitlesize)

        #
                    im = ax_long.imshow(field_long,aspect='auto',extent=[xmin,xmax,ymin,ymax],vmax=max_f,vmin=min_f)
                    im = ax_rho.imshow(field_rho,aspect='auto',extent=[xmin,xmax,ymin,ymax],vmax=max_f,vmin=min_f)
                    im = ax_phi.imshow(field_phi,aspect='auto',extent=[xmin,xmax,ymin,ymax],vmax=max_f,vmin=min_f)
        #
                    cbar = fig.colorbar(im, cax = ax_bar)
        #
                    ax_long.set_ylabel(y_label,fontsize=axislabelsize)
                    ax_long.set_xlabel(x_label,fontsize=axislabelsize)
                    ax_rho.set_xlabel(x_label,fontsize=axislabelsize)
                    ax_phi.set_xlabel(x_label,fontsize=axislabelsize)
        #
                    ax_long.set_title(f"|{ax_title_name}"+"$_{z}$|",fontsize=axistitlesize,pad=20)
                    ax_rho.set_title(f"|{ax_title_name}"+"$_{\\rho}$|",fontsize=axistitlesize,pad=20)
                    ax_phi.set_title(f"|{ax_title_name}"+"$_{\\phi}$|",fontsize=axistitlesize,pad=20)
        #
        #
                    ax_long.tick_params(which="major",axis='both',labelsize=ticksize)
                    ax_rho.tick_params(which="major",axis='both',labelsize=ticksize)
                    ax_phi.tick_params(which="major",axis='both',labelsize=ticksize)
        #
                    ax_rho.set_yticklabels([])
                    ax_phi.set_yticklabels([])
        #
                    ax_bar.tick_params(which='major', axis='both',labelsize=ticksize)
                    ax_bar.set_ylabel(cbar_title,fontsize=axislabelsize)
                    fig.tight_layout()
                    #fig.set_facecolor('gray')
        #
                    filename = f"{path}/f_{kind}-ax_{axis}-slc_{data_slice}-ti_{str(ti).zfill(5)}.png"
                    plt.show()
                    plt.savefig(filename)
                    plt.close()
                # Make the __plot funciton delayed so can be excuted lazily.
                d_plot = dask.delayed(__plot)
                data_geom = "data_cyl" if not kind == "j" else "data_cart"
                field_list = [self.select_field[kind][data_geom][datanames[0]],
                              self.select_field[kind][data_geom][datanames[1]],
                              self.select_field[kind][data_geom][datanames[2]]]
                path = f"{self.basepath}/tmp/{kind}_{axis}_{data_slice}/"
                self._create_folder(path)
                # Check if we have a maximum value
                try:
                    maxf = np.max(np.array([self.max_values[self.basepath][datanames[0]][f'global'],
                                             self.max_values[self.basepath][datanames[1]][f'global'],
                                             self.max_values[self.basepath][datanames[2]][f'global']]))
                # If not use a default one
                except:
                    maxf = 0.1
                print(maxf)
                # Queue all the plots.
                ops = [d_plot([np.abs(field_list[0][i]), np.abs(field_list[1][i]),np.abs(field_list[2][i])],
                              kind,axis,data_slice,datanames,path, __select_fields,self.select_axis,maxf,self.t[i], i) for i in range(len(self.t))]
                print("plotting")
                dask.compute(*ops)
                plt.close('all')

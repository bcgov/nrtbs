import matplotlib.pyplot as plt
import matplotlib.patches as patches
from dNBR import NBR
from operator import add, sub
import datetime
import numpy as np
import math

filenames = ['S2B_MSIL1C_20210626T185919_N0300_R013_T10UFB_20210626T211041.bin',
             'S2B_MSIL1C_20210629T190919_N0300_R056_T10UFB_20210629T212050.bin',
             'S2A_MSIL1C_20210701T185921_N0301_R013_T10UFB_20210701T223921.bin',
             'S2B_MSIL1C_20210709T190919_N0301_R056_T10UFB_20210709T224644.bin',
             'S2A_MSIL1C_20210714T190921_N0301_R056_T10UFB_20210714T225634.bin',
             'S2B_MSIL1C_20210719T190919_N0301_R056_T10UFB_20210719T212141.bin',
             'S2A_MSIL1C_20210724T190921_N0301_R056_T10UFB_20210724T230122.bin',
             'S2B_MSIL1C_20210726T185919_N0301_R013_T10UFB_20210726T211239.bin',
             'S2B_MSIL1C_20210729T190919_N0301_R056_T10UFB_20210729T212314.bin',
             'S2A_MSIL1C_20210803T190921_N0301_R056_T10UFB_20210803T224926.bin',
             'S2B_MSIL1C_20210805T185919_N0301_R013_T10UFB_20210805T211134.bin',
             'S2A_MSIL1C_20210813T190921_N0301_R056_T10UFB_20210813T224901.bin',
             'S2A_MSIL1C_20210902T190911_N0301_R056_T10UFB_20210902T225534.bin',
             'S2B_MSIL1C_20210907T190929_N0301_R056_T10UFB_20210907T224046.bin']


fig, ((ax1,ax2),(ax3,ax4),(ax5,ax6)) = plt.subplots(3, 2, figsize=(15,8))
clicks = []
plot_colors = ['b','r','y','k','c','m']

def interactive_time_serise(file,plot_type:str('image or nbr'), file_list, width):
    '''
    '''
    global params
    params = [NBR(f'raster_data/small/{file}') for file in file_list]
    
    global square_width
    square_width = width
    
    if plot_type == 'image':
        data = NBR(file)
        image = np.stack([scale(data[0]),scale(data[1]),scale(data[2])], axis=2)
        ax1.imshow(image)
    
    elif plot_type == 'nbr':
        image = NBR(file)[4]
        ax1.imshow(image, cmap='grey')
        
    else:
        print('invalid image type')
    
    cid = fig.canvas.mpl_connect('button_press_event', on_click)
    
    plt.show()
    
def param_plots(clicks, width):
    '''
    takes the list of click locations and square_width and plots the B12, B11, B09, B08, and NBR of the mean value timeserise in a box with side lenght = square_width
    '''
    ax = [ax2,ax3,ax4,ax5,ax6]
    band_names = ['B12', 'B11', 'B09', 'B08', 'NBR']
    b = [[] for i in range(len(band_names))]
    mean = [[] for i in range(len(band_names))]
    std = [[] for i in range(len(band_names))]
    
    time = []
    y = int(clicks[-1][1])
    x = int(clicks[-1][0])
    
    for file in range(len(params)):#loops finding pixel values for each parameter in the square
        for band in range(len(band_names)):
            b[band] = []
        
        date  = datetime.datetime.strptime(filenames[file].split('_')[2].split('T')[0],'%Y%m%d')
        for i in range(y,y+width):
            for j in range(x,x+width):
                for n in range(len(band_names)):
                    b[n] += [params[file][n][i][j]]
                    
        for band in range(len(band_names)):
            mean[band] += [np.nanmean(b[band])]
            std[band] += [np.nanstd(b[band])]        
        time += [date]

    
    for band in range(len(band_names)): #plotting each time serise
        ax[band].plot(time, mean[band], color=f'{plot_colors[len(clicks)-1]}',label=f'Mean at ({x},{y})')
        ax[band].plot(time, list(map(add,mean[band], std[band])), color=f'{plot_colors[len(clicks)-1]}', linestyle='dashed')
        ax[band].plot(time, list(map(sub,mean[band], std[band])), color=f'{plot_colors[len(clicks)-1]}', linestyle='dotted')

        ax[band].legend()
        ax[band].set_title(band_names[band])

    plt.tight_layout()
    plt.show()
'''
def gui(file,file_type):
    data = NBR(file)
    if file_type == 'B12':
    ax1.imshow(nbr[4], cmap='grey')
'''

def on_click(event):
    print(f"Clicked at: {event.xdata}, {event.ydata}")
    if event.inaxes is not None and len(clicks) < 6:  # Check if the click is inside the plot area
        # Store the click coordinates
        clicks.append((event.xdata, event.ydata))
        print(f"Clicked at: {event.xdata}, {event.ydata}")
        
        # Create a square patch
        square = patches.Rectangle((event.xdata, event.ydata), square_width, square_width, 
                                   linewidth=1, edgecolor=f'{plot_colors[len(clicks)-1]}', facecolor='none')
        ax1.add_patch(square)  # Add the square to the plot
        fig.canvas.draw()  # Update the plot
        param_plots(clicks,square_width)
        
def scale(X):
    # default: scale a band to [0, 1]  and then clip
    mymin = np.nanmin(X) # np.nanmin(X))
    mymax = np.nanmax(X) # np.nanmax(X))
    X = (X-mymin) / (mymax - mymin)  # perform the linear transformation

    X[X < 0.] = 0.  # clip
    X[X > 1.] = 1.

    # use histogram trimming / turn it off to see what this step does!
    if  True:
        values = X.ravel().tolist()
        values.sort()
        n_pct = 1. # percent for stretch value
        frac = n_pct / 100.
        lower = int(math.floor(float(len(values))*frac))
        upper = int(math.floor(float(len(values))*(1. - frac)))
        mymin, mymax = values[lower], values[upper]
        X = (X-mymin) / (mymax - mymin)  # perform the linear transformation
    
    return X



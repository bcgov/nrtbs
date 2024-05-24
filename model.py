from misc import exist, read_hdr, read_float, hdr_fn, read_binary
import numpy as np
import matplotlib.pyplot as plt
import math
import sys
from osgeo import gdal

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
    

def plot(file_name):
    '''
    takes binary raster file and plots a 2d heat map using the B12, B11, and B09
    '''
    vals = read_binary(file_name)
    data = vals[3]
    width = vals[0]
    height = vals[1]
    band1grid = np.zeros((width,height))
    band2grid = np.zeros((width,height))
    band3grid = np.zeros((width,height))
    for i in range(width):
        for j in range(height):
            band1grid[i][j] = data[width*height*0 + width*i+j]
            band2grid[i][j] = data[width*height*1 + width*i+j]
            band3grid[i][j] = data[width*height*2 + width*i+j]
    band1 = scale(band1grid)
    band2 = scale(band2grid)
    band3 = scale(band3grid)
    image = np.stack([band1,band2,band3], axis=2)
    plt.imshow(image)
    #plt.title(sys.argv[1] + " with encoding R,G,B =(B12, B11, B9)")
    #plt.axis('off')  # Turn off axis labels
    plt.tight_layout()
    plt.show()
    
    
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
import matplotlib.colors
import os
import numpy as np
from numpy.ma import masked_where

# Path to your .tif file
tif_path = '/Users/sterlingvondehn/Downloads/G90267 2/barc/BARC_G90267_20240420_20240619_S2.tif'
title = 'non_clipped_fort_nelson_BARC'
start_date = 20240420
end_date = 20240619

# Open the .tif file using rasterio
with rasterio.open(tif_path) as src:
    # Read the first band
    band1 = src.read(1)
    masked_band1 = masked_where(band1>4, band1)

    # Plot the image using matplotlib
    cmap = matplotlib.colors.ListedColormap(['green','yellow','orange','red'])   #plotting
    plt.figure(figsize=(15,15))
    plt.imshow(masked_band1,vmin=1,vmax=4,cmap=cmap)
    plt.title(f'BARC 256 burn severity, start date: {start_date}, end date: {end_date}')
    plt.scatter(np.nan,np.nan,marker='s',s=100,label=f'Unburned',color='green')
    plt.scatter(np.nan,np.nan,marker='s',s=100,label=f'Low' ,color='yellow')
    plt.scatter(np.nan,np.nan,marker='s',s=100,label=f'Medium',color='orange')
    plt.scatter(np.nan,np.nan,marker='s',s=100,label=f'High',color='red')
    plt.legend(fontsize="20")
    #plt.show()
    plt.tight_layout()
    plt.savefig(f'{title}.png')
from misc import exist, read_hdr, read_float, hdr_fn, read_binary
import numpy as np
import matplotlib.pyplot as plt
import math
import os
from dNBR import dNBR, NBR

def burnmask(start_file,end_file,threshold):
    '''
    creates a burn mask of the provided fire using the fire start and end frames and provided dNBR threshold
    >>>burnmask('raster_data/small/S2B_MSIL1C_20210626T185919_N0300_R013_T10UFB_20210626T211041.bin', 'raster_data/small/S2B_MSIL1C_20210907T190929_N0301_R056_T10UFB_20210907T224046.bin')
    '''
    vals = read_binary(start_file) 
    width = vals[0]
    height = vals[1]
    dnbr = dNBR(start_file,end_file)
    mask = np.zeros((height,width))
    for i in range(height):
        for j in range(width):
            if dnbr[i][j] >= threshold: #selecting pixels with dNBR >= 0.2 and discading the rest
                mask[i][j] = 1
            else:
                mask[i][j] = np.nan
    plt.figure(figsize=(15,15))
    plt.imshow(mask, cmap='grey')
    plt.title(f'Fire mask using threshold: {threshold}')
    plt.tight_layout()
    plt.savefig(f'Fire_mask_{threshold}.png')
from misc import exist, read_hdr, read_float, hdr_fn, read_binary
import numpy as np
import matplotlib.pyplot as plt
import math
import os
from dNBR import dNBR, NBR
from operator import add, sub
import datetime

def burnmask(start_file,end_file,threshold):
    '''
    creates a burn mask of the provided fire using the fire start and end frames and provided dNBR threshold
    >>>burnmask('raster_data/small/S2B_MSIL1C_20210626T185919_N0300_R013_T10UFB_20210626T211041.bin', 'raster_data/small/S2B_MSIL1C_20210907T190929_N0301_R056_T10UFB_20210907T224046.bin')
    '''
    vals = read_binary(f'raster_data/small/{start_file}') 
    width = vals[0]
    height = vals[1]
    dnbr = dNBR(f'raster_data/small/{start_file}',f'raster_data/small/{end_file}')
    mask = dnbr >= threshold
    '''
    plt.figure(figsize=(15,15))
    plt.imshow(mask, cmap='grey')
    plt.title(f'Fire mask using threshold: {threshold}')
    plt.tight_layout()
    plt.savefig(f'Fire_mask_{threshold}.png')
    '''
    return mask
    
    
def param_plots(file_list,threshold):
    '''
    Makes plots of the burned and unburned mean and standard deveation of the 4 parameters calculated using the NBR function, B12, B11, B09, B08, and NBR.
    '''
    '''
    burned_b12 = []; burned_b11 = []; burned_b09 = []; burned_b08 = []; burned_nbr = []; unburned_b12 = []; unburned_b11 = []; unburned_b09 = []; unburned_b08 = []; unburned_nbr = []
    
    burn12_mean = []; burn11_mean = []; burn09_mean = []; burn08_mean = []; burnnbr_mean = []; unburn12_mean = []; unburn11_mean = []; unburn09_mean = [];unburn08_mean = []; unburnnbr_mean = []
        
    burn12_dev = []; burn11_dev = []; burn09_dev = []; burn08_dev = []; burnnbr_dev = []; unburn12_dev = []; unburn11_dev = []; unburn09_dev = [];unburn08_dev = []; unburnnbr_dev = []
        

    burned_band_list = [burned_b12,burned_b11,burned_b09,burned_b08,burned_nbr]
    unburned_band_list = [unburned_b12, unburned_b11, unburned_b09, unburned_b08, unburned_nbr]

    
    mean_burned_band_list = [burn12_mean, burn11_mean, burn09_mean, burn08_mean, burnnbr_mean]
    mean_unburned_band_list = [unburn12_mean, unburn11_mean, unburn09_mean, unburn08_mean, unburnnbr_mean]
    std_burned_band_list = [burn12_dev, burn11_dev, burn09_dev, burn08_dev, burnnbr_dev]
    std_unburned_band_list = [unburn12_dev, unburn11_dev, unburn09_dev, unburn08_dev, unburnnbr_dev]
    '''
    
    band_names = ['B12', 'B11', 'B09', 'B08', 'NBR']
    burned_b = [[] for i in range(len(band_names))]
    unburned_b = [[] for i in range(len(band_names))]
    burned_mean = [[] for i in range(len(band_names))]
    unburned_mean = [[] for i in range(len(band_names))]
    burned_std = [[] for i in range(len(band_names))]
    unburned_std = [[] for i in range(len(band_names))]
    
    mask = burnmask(file_list[0],file_list[-1],threshold) #calculating the mask ie. where is burned/unburned
    
    time = []
    
    start_date = datetime.datetime.strptime(file_list[0].split('_')[2].split('T')[0],'%Y%m%d') #fire start date
    
    for file in file_list:#loops finding pixel values for each parameter and sorting them to burned or unburned
        for band in range(len(band_names)):
            burned_b[band] = []
            unburned_b[band] = []
        
        date  = datetime.datetime.strptime(file.split('_')[2].split('T')[0],'%Y%m%d')
        params = NBR(f'raster_data/small/{file}')
        for i in range(len(mask)):
            for j in range(len(mask[0])):
                for band in range(len(band_names)):
                    if mask[i][j]:
                        burned_b[band] += [params[band][i][j]]
                    else:
                        unburned_b[band] += [params[band][i][j]]
                        
        for band in range(5):
            burned_mean[band] += [np.nanmean(burned_b[band])]
            burned_std[band] += [np.nanstd(burned_b[band])]
            
            unburned_mean[band] += [np.nanmean(unburned_b[band])]
            unburned_std[band] += [np.nanstd(unburned_b[band])]   
            
        time += [date]

    plt.figure(figsize=(15,15)) #plotting
    
    band_title = ['B12', 'B11', 'B09', 'B08', 'NBR']
    for band in range(len(band_names)):
        plt.plot(time, burned_mean[band], color='red',label='Burned mean')
        plt.plot(time, list(map(add,burned_mean[band], burned_std[band])), color='red', linestyle='dashed', label='Burned mean +')
        plt.plot(time, list(map(sub,burned_mean[band], burned_std[band])), color='red', linestyle='dotted', label='Burned mean -')
        
        plt.plot(time, unburned_mean[band], color='green',label='Unburned mean')
        plt.plot(time, list(map(add, unburned_mean[band], unburned_std[band])), color='green', linestyle='dashed', label='Unburned mean +')
        plt.plot(time, list(map(sub,unburned_mean[band], unburned_std[band])), color='green', linestyle='dotted', label='Unburned mean -')            
        plt.legend()
        plt.title(f'{band_title[band]} burned and unburned')
        plt.tight_layout()
        plt.savefig(f'{band_title[band]}.png')
        plt.clf()

filenames = ['S2B_MSIL1C_20210626T185919_N0300_R013_T10UFB_20210626T211041.bin','S2B_MSIL1C_20210629T190919_N0300_R056_T10UFB_20210629T212050.bin','S2A_MSIL1C_20210701T185921_N0301_R013_T10UFB_20210701T223921.bin','S2B_MSIL1C_20210709T190919_N0301_R056_T10UFB_20210709T224644.bin','S2A_MSIL1C_20210714T190921_N0301_R056_T10UFB_20210714T225634.bin','S2B_MSIL1C_20210719T190919_N0301_R056_T10UFB_20210719T212141.bin','S2A_MSIL1C_20210724T190921_N0301_R056_T10UFB_20210724T230122.bin','S2B_MSIL1C_20210726T185919_N0301_R013_T10UFB_20210726T211239.bin','S2B_MSIL1C_20210729T190919_N0301_R056_T10UFB_20210729T212314.bin','S2A_MSIL1C_20210803T190921_N0301_R056_T10UFB_20210803T224926.bin','S2B_MSIL1C_20210805T185919_N0301_R013_T10UFB_20210805T211134.bin','S2A_MSIL1C_20210813T190921_N0301_R056_T10UFB_20210813T224901.bin','S2A_MSIL1C_20210902T190911_N0301_R056_T10UFB_20210902T225534.bin','S2B_MSIL1C_20210907T190929_N0301_R056_T10UFB_20210907T224046.bin']
param_plots(filenames,.2)
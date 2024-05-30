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
    mask = np.zeros((height,width))
    for i in range(height):
        for j in range(width):
            if dnbr[i][j] >= threshold: #selecting pixels with dNBR >= threshold and discading the rest
                mask[i][j] = True
            else:
                mask[i][j] = False
    '''
    plt.figure(figsize=(15,15))
    plt.imshow(mask, cmap='grey')
    plt.title(f'Fire mask using threshold: {threshold}')
    plt.tight_layout()
    plt.savefig(f'Fire_mask_{threshold}.png')
    '''
    return mask
    
    
def param_plots(file_list,threshold):
    mask = burnmask(file_list[0],file_list[-1],threshold)
    
    burn12_mean = []; burn11_mean = []; burn09_mean = []; burn08_mean = []; burnnbr_mean = []; unburn12_mean = []; unburn11_mean = []; unburn09_mean = [];unburn08_mean = []; unburnnbr_mean = []
    
    burn12_dev = []; burn11_dev = []; burn09_dev = []; burn08_dev = []; burnnbr_dev = []; unburn12_dev = []; unburn11_dev = []; unburn09_dev = [];unburn08_dev = []; unburnnbr_dev = []
    
    time = []
    
    start_date = datetime.datetime.strptime(file_list[0].split('_')[2].split('T')[0],'%Y%m%d')
    
    for file in file_list:    
        burned_b12 = []; burned_b11 = []; burned_b09 = []; burned_b08 = []; burned_nbr = []; unburned_b12 = []; unburned_b11 = []; unburned_b09 = []; unburned_b08 = []; unburned_nbr = []
        
        date  = datetime.datetime.strptime(file.split('_')[2].split('T')[0],'%Y%m%d')
        params = NBR(f'raster_data/small/{file}')
        for i in range(len(mask[0])):
            for j in range(len(mask)):
                if mask[i][j]:
                    if not np.isnan(params[0][i][j]):
                        burned_b12 += [params[0][i][j]]
                    if not np.isnan(params[1][i][j]):
                        burned_b11 += [params[1][i][j]]
                    if not np.isnan(params[2][i][j]):
                        burned_b09 += [params[2][i][j]]
                    if not np.isnan(params[3][i][j]):
                        burned_b08 += [params[3][i][j]]
                    if not np.isnan(params[4][i][j]):
                        burned_nbr += [params[4][i][j]]
                else:
                    if not np.isnan(params[0][i][j]):
                        unburned_b12 += [params[0][i][j]]
                    if not np.isnan(params[1][i][j]):
                        unburned_b11 += [params[1][i][j]]
                    if not np.isnan(params[2][i][j]):
                        unburned_b09 += [params[2][i][j]]
                    if not np.isnan(params[3][i][j]):
                        unburned_b08 += [params[3][i][j]]
                    if not np.isnan(params[4][i][j]):
                        unburned_nbr += [params[4][i][j]]
        burn12_mean += [np.mean(burned_b12)]
        burn11_mean += [np.mean(burned_b11)]
        burn09_mean += [np.mean(burned_b09)]
        burn08_mean += [np.mean(burned_b08)]
        burnnbr_mean += [np.mean(burned_nbr)]
        
        burn12_dev += [np.std(burned_b12)]
        burn11_dev += [np.std(burned_b11)]
        burn09_dev += [np.std(burned_b09)]
        burn08_dev += [np.std(burned_b08)]
        burnnbr_dev += [np.std(burned_nbr)]
        
        days = date.day - start_date.day
        months = date.month - start_date.month
        time += [days + months*31]
            
        unburn12_mean += [np.mean(unburned_b12)]
        unburn11_mean += [np.mean(unburned_b11)]
        unburn09_mean += [np.mean(unburned_b09)]
        unburn08_mean += [np.mean(unburned_b08)]
        unburnnbr_mean += [np.mean(unburned_nbr)]
        
        unburn12_dev += [np.std(unburned_b12)]
        unburn11_dev += [np.std(unburned_b11)]
        unburn09_dev += [np.std(unburned_b09)]
        unburn08_dev += [np.std(unburned_b08)]
        unburnnbr_dev += [np.std(unburned_nbr)]
        
    plt.figure(figsize=(15,15))
    
    plt.plot(time, burn12_mean, color='red', label='Burned mean')
    plt.plot(time, list(map(add,burn12_mean, burn12_dev)), color='red', linestyle='dashed')
    plt.plot(time, list(map(sub,burn12_mean, burn12_dev)), color='red', linestyle='dotted')
        
    plt.plot(time, unburn12_mean, color='green', label='Unburned mean')
    plt.plot(time, list(map(add,unburn12_mean, unburn12_dev)), color='green', linestyle='dashed')
    plt.plot(time, list(map(sub,unburn12_mean, unburn12_dev)), color='green', linestyle='dotted')      
    plt.legend()
    plt.title(f'B12 burned and unburned')
    plt.tight_layout()
    plt.savefig(f'B12.png')
    plt.clf()
    
    
    
    plt.plot(time, burn11_mean, color='red', label='Burned mean')
    plt.plot(time, list(map(add,burn11_mean, burn11_dev)), color='red', linestyle='dashed')
    plt.plot(time, list(map(sub,burn11_mean, burn11_dev)), color='red', linestyle='dotted')
        
    plt.plot(time, unburn11_mean, color='green', label='Unburned mean')
    plt.plot(time, list(map(add,unburn11_mean, unburn11_dev)), color='green', linestyle='dashed')
    plt.plot(time, list(map(sub,unburn11_mean, unburn11_dev)), color='green', linestyle='dotted')      
    plt.legend()
    plt.title(f'B11 burned and unburned')
    plt.tight_layout()
    plt.savefig(f'B11.png')
    plt.clf()
    
    
    
    plt.plot(time, burn09_mean, color='red', label='Burned mean')
    plt.plot(time, list(map(add,burn09_mean, burn09_dev)), color='red', linestyle='dashed')
    plt.plot(time, list(map(sub,burn09_mean, burn09_dev)), color='red', linestyle='dotted')
        
    plt.plot(time, unburn09_mean, color='green', label='Unburned mean')
    plt.plot(time, list(map(add,unburn09_mean, unburn09_dev)), color='green', linestyle='dashed')
    plt.plot(time, list(map(sub,unburn09_mean, unburn09_dev)), color='green', linestyle='dotted')      
    plt.legend()
    plt.title(f'B09 burned and unburned')
    plt.tight_layout()
    plt.savefig(f'B09.png') 
    plt.clf()
    
    
    
    plt.plot(time, burn08_mean, color='red', label='Burned mean')
    plt.plot(time, list(map(add,burn08_mean, burn08_dev)), color='red', linestyle='dashed')
    plt.plot(time, list(map(sub,burn08_mean, burn08_dev)), color='red', linestyle='dotted')
        
    plt.plot(time, unburn08_mean, color='green', label='Unburned mean')
    plt.plot(time, list(map(add,unburn08_mean, unburn08_dev)), color='green', linestyle='dashed')
    plt.plot(time, list(map(sub,unburn08_mean, unburn08_dev)), color='green', linestyle='dotted')      
    plt.legend()
    plt.title(f'B08 burned and unburned')
    plt.tight_layout()
    plt.savefig(f'B08.png')   
    plt.clf()
    
    
    
    plt.plot(time, burnnbr_mean, color='red', label='Burned mean')
    plt.plot(time, list(map(add,burnnbr_mean, burnnbr_dev)), color='red', linestyle='dashed')
    plt.plot(time, list(map(sub,burnnbr_mean, burnnbr_dev)), color='red', linestyle='dotted')
    
    plt.plot(time, unburnnbr_mean, color='green', label='Unburned mean')
    plt.plot(time, list(map(add,unburnnbr_mean, unburnnbr_dev)), color='green', linestyle='dashed')
    plt.plot(time, list(map(sub,unburnnbr_mean, unburnnbr_dev)), color='green', linestyle='dotted')   
    plt.legend()
    plt.title(f'NBR burned and unburned')
    plt.tight_layout()
    plt.savefig(f'NBR.png')    
    plt.clf()


filenames = ['S2B_MSIL1C_20210626T185919_N0300_R013_T10UFB_20210626T211041.bin','S2B_MSIL1C_20210629T190919_N0300_R056_T10UFB_20210629T212050.bin','S2A_MSIL1C_20210701T185921_N0301_R013_T10UFB_20210701T223921.bin','S2B_MSIL1C_20210709T190919_N0301_R056_T10UFB_20210709T224644.bin','S2A_MSIL1C_20210714T190921_N0301_R056_T10UFB_20210714T225634.bin','S2B_MSIL1C_20210719T190919_N0301_R056_T10UFB_20210719T212141.bin','S2A_MSIL1C_20210724T190921_N0301_R056_T10UFB_20210724T230122.bin','S2B_MSIL1C_20210726T185919_N0301_R013_T10UFB_20210726T211239.bin','S2B_MSIL1C_20210729T190919_N0301_R056_T10UFB_20210729T212314.bin','S2A_MSIL1C_20210803T190921_N0301_R056_T10UFB_20210803T224926.bin','S2B_MSIL1C_20210805T185919_N0301_R013_T10UFB_20210805T211134.bin','S2A_MSIL1C_20210813T190921_N0301_R056_T10UFB_20210813T224901.bin','S2A_MSIL1C_20210902T190911_N0301_R056_T10UFB_20210902T225534.bin','S2B_MSIL1C_20210907T190929_N0301_R056_T10UFB_20210907T224046.bin']
param_plots(filenames,.2)

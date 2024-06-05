from misc import exist, read_hdr, read_float, hdr_fn, read_binary
import numpy as np
import matplotlib.pyplot as plt


def NBR(file_name):
    '''
    Takes binary file and returns the band values as well as the NBR.
    >>> NBR('S2A_MSIL1C_20210902T190911_N0301_R056_T10UFB_20210902T225534.bin')
    '''
    vals = read_binary(file_name) 
    data = vals[3]
    width = vals[0]
    height = vals[1]
    NBR = np.zeros((height,width))    
    B12 = np.zeros((height,width))
    B11 = np.zeros((height,width))
    B09 = np.zeros((height,width))
    B08 = np.zeros((height,width))
    for i in range(height):
        for j in range(width):
            B12[i][j] = data[width*height*0 + width*i+j]
            B11[i][j] = data[width*height*1 + width*i+j]
            B09[i][j] = data[width*height*2 + width*i+j]
            B08[i][j] = data[width*height*3 + width*i+j]
    NBR = (B08-B12)/(B08+B12)        
    date  = file_name.split('_')[2].split('T')[0]
    '''
    plt.figure(figsize=(15,15))
    plt.imshow(NBR, cmap='Greys')
    plt.title(f'NBR of Sparks Lake fire on {date}')
    plt.tight_layout()
    plt.colorbar()
    '''
    return [B12,B11,B09,B08,NBR,height,width]
            
            
def dNBR(start_frame, end_frame):
    '''
    Takes the start and end binary files and returns the dNRB.
    >>> dNBR('S2B_MSIL1C_20210626T185919_N0300_R013_T10UFB_20210626T211041.bin', 'S2A_MSIL1C_20210907T190911_N0301_R056_T10UFB_20210902T225534.bin')
    '''
    preNBR = NBR(start_frame)[4]
    postNBR = NBR(end_frame)[4]
    dNBR = postNBR - preNBR
    date  = end_frame.split('_')[2].split('T')[0]
    '''
    #plt.figure(figsize=(15,15))
    plt.imshow(dNBR, cmap='Greys')
    plt.title(f'dNBR of Sparks Lake fire using end date: {date}')
    plt.colorbar()
    plt.tight_layout()
    plt.show()
    #plt.savefig(f'{end_frame}dNBR.png')    
    '''
    return dNBR

'''
preNBR = NBR('S2B_MSIL1C_20210626T185919_N0300_R013_T10UFB_20210626T211041.bin')[4]

filenames = ['S2B_MSIL1C_20210626T185919_N0300_R013_T10UFB_20210626T211041.bin','S2B_MSIL1C_20210629T190919_N0300_R056_T10UFB_20210629T212050.bin','S2A_MSIL1C_20210701T185921_N0301_R013_T10UFB_20210701T223921.bin','S2B_MSIL1C_20210709T190919_N0301_R056_T10UFB_20210709T224644.bin','S2A_MSIL1C_20210714T190921_N0301_R056_T10UFB_20210714T225634.bin','S2B_MSIL1C_20210719T190919_N0301_R056_T10UFB_20210719T212141.bin','S2A_MSIL1C_20210724T190921_N0301_R056_T10UFB_20210724T230122.bin','S2B_MSIL1C_20210726T185919_N0301_R013_T10UFB_20210726T211239.bin','S2B_MSIL1C_20210729T190919_N0301_R056_T10UFB_20210729T212314.bin','S2A_MSIL1C_20210803T190921_N0301_R056_T10UFB_20210803T224926.bin','S2B_MSIL1C_20210805T185919_N0301_R013_T10UFB_20210805T211134.bin','S2A_MSIL1C_20210813T190921_N0301_R056_T10UFB_20210813T224901.bin','S2A_MSIL1C_20210902T190911_N0301_R056_T10UFB_20210902T225534.bin','S2B_MSIL1C_20210907T190929_N0301_R056_T10UFB_20210907T224046.bin']

for file in filenames:
    dNBR('S2B_MSIL1C_20210626T185919_N0300_R013_T10UFB_20210626T211041.bin',file)

'''
'''
err = dNBR('raster_data/S2B_MSIL1C_20210626T185919_N0300_R013_T10UFB_20210626T211041.bin','raster_data/S2B_MSIL1C_20210907T190929_N0301_R056_T10UFB_20210907T224046.bin') - dNBR('raster_data/S2B_MSIL1C_20210626T185919_N0300_R013_T10UFB_20210626T211041.bin','raster_data/S2A_MSIL1C_20210813T190921_N0301_R056_T10UFB_20210813T224901.bin')

plt.imshow(err)
plt.show()
'''
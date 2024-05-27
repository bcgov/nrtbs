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
    NBR = np.zeros((width,height))    
    B12 = np.zeros((width,height))
    B11 = np.zeros((width,height))
    B09 = np.zeros((width,height))
    B08 = np.zeros((width,height))
    for i in range(width):
        for j in range(height):
            if (data[width*height*0 + width*i+j] + data[width*height*3 + width*i+j]) == 0:
                 NBR[i][j] = 0
            else:
                NBR[i][j] = (data[width*height*0 + width*i+j] - data[width*height*3 + width*i+j])/(data[width*height*0 + width*i+j] + data[width*height*3 + width*i+j])
            B12[i][j] = data[width*height*0 + width*i+j]
            B11[i][j] = data[width*height*1 + width*i+j]
            B09[i][j] = data[width*height*2 + width*i+j]
            B08[i][j] = data[width*height*3 + width*i+j]
    return [B12,B11,B09,B08,NBR]
            
            
def dNBR(start_frame, end_frame):
    '''
    Takes the start and end binary files and returns the dNRB.
    >>> dNBR('S2B_MSIL1C_20210626T185919_N0300_R013_T10UFB_20210626T211041.bin', 'S2A_MSIL1C_20210907T190911_N0301_R056_T10UFB_20210902T225534.bin')
    '''
    preNBR = NBR(start_frame)[4]
    postNBR = NBR(end_frame)[4]
    dNBR = postNBR - preNBR
    plt.imshow(dNBR, cmap='Greys')
    plt.show()

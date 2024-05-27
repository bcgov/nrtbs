from misc import exist, read_hdr, read_float, hdr_fn, read_binary
import numpy as np
import matplotlib.pyplot as plt
import math
import os


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
    

def plot(file_list):
    '''
    Takes a list of binary raster files organized by date and plots an image using the B12, B11, and B09 bands. Also plots the NBR of each frame as well as the dNBR of each frame except the first (first frame would have dNBR=0). Function places each files into three directories: 'images', 'NBR', and 'dNBR'.
    >>> plot(['S2B_MSIL1C_20210626T185919_N0300_R013_T10UFB_20210626T211041.bin',...,'S2B_MSIL1C_20210907T190929_N0301_R056_T10UFB_20210907T224046.bin'])
    '''
    for n in range(len(file_list)):
        vals = read_binary(file_list[n]) #reading each file
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
                    NBR[i][j] = (data[width*height*0 + width*i+j] - data[width*height*3 + width*i+j])/(data[width*height*0 + width*i+j] + data[width*height*3 + width*i+j]) #calculating the NBR
                B12[i][j] = data[width*height*0 + width*i+j] #updating band data for each of the 4 bands
                B11[i][j] = data[width*height*1 + width*i+j]
                B09[i][j] = data[width*height*2 + width*i+j]
                B08[i][j] = data[width*height*3 + width*i+j]
                
        band1 = scale(B12) #scaling bands for plotting
        band2 = scale(B11)
        band3 = scale(B09)
        band4 = scale(B08)
        date  = file_list[n].split('_')[2].split('T')[0]
        image = np.stack([band1,band2,band3], axis=2) #creating 3D matrix for RGB plot
        
        plt.figure(figsize=(15,15)) #setting figure parameters
        plt.tight_layout()
        
        plt.imshow(image) #Plotting the image
        plt.title(f'Sparks Lake fire on {date}, bands: r=B12, g=B11, b=B09')
        plt.tight_layout()
        if not os.path.exists('images'):
            os.mkdir('images')
        plt.savefig(f'images/{date}_{file_list[n]}.png')
        
        plt.imshow(NBR, cmap='Greys') #Plotting the NBR
        plt.title(f'NBR of Sparks Lake fire on {date}')
        plt.tight_layout()
        plt.colorbar()      
        if not os.path.exists('NBR'):
            os.mkdir('NBR')
        plt.savefig(f'NBR/{date}_{file_list[n]}.png')
        
        #Plotting the dNBR for all frames but the first
        if n == 0:
            start_NBR = NBR
        else:
            dNBR = start_NBR - NBR        
            plt.imshow(dNBR, cmap='Greys')
            plt.title(f'dNBR of Sparks Lake fire on {date}')
            plt.tight_layout()     
            if not os.path.exists('dNBR'):
                os.mkdir('dNBR')
            plt.savefig(f'dNBR/{date}_{file_list[n]}.png')

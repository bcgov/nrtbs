from misc import exist, read_hdr, read_float, hdr_fn, read_binary, extract_date
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import datetime

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
        n_pct = .01 # percent for stretch value
        frac = n_pct / 100.
        lower = int(math.floor(float(len(values))*frac))
        upper = int(math.floor(float(len(values))*(1. - frac)))
        mymin, mymax = values[lower], values[upper]
        X = (X-mymin) / (mymax - mymin)  # perform the linear transformation
    
    return X

def plot(file_dir,title='No title given'):
    '''
    Takes a directory containing bin files and plots an image using the B12, B11, and B09 bands. Also plots the NBR of each frame as well as the dNBR of each frame except the first (first frame would have dNBR=0). Function places each files into three directories: 'images', 'NBR', and 'dNBR'.
    >>> plot('raster_data')
    '''
    #extracting bin files
    files = os.listdir(file_dir)
    file_list = []
    for n in range(len(files)):
        if files[n].split('.')[-1] == 'bin':
            file_list.append(files[n])
        else:
            continue;
    

    sorted_file_names = sorted(file_list, key=extract_date) #sorting
   

    for n in range(len(sorted_file_names)):
        vals = read_binary(f'{file_dir}/{sorted_file_names[n]}') #reading each file
        data = vals[3]
        width = vals[0]
        height = vals[1]
        bands = vals[2]
        if bands < 4:
            B12 = np.zeros((height,width))
            B11 = np.zeros((height,width))
            B09 = np.zeros((height,width))
            for i in range(height):
                for j in range(width):
                    B12[i][j] = data[width*height*0 + width*i+j] #updating band data for each of the 4 bands
                    B11[i][j] = data[width*height*1 + width*i+j]
                    B09[i][j] = data[width*height*2 + width*i+j]
            band1 = scale(B12) #scaling bands for plotting
            band2 = scale(B11)
            band3 = scale(B09)
            date  = extract_date(sorted_file_names[n])
            image = np.stack([band1,band2,band3], axis=2) #creating 3D matrix for RGB plot
            
            plt.figure(figsize=(15,15)) #setting figure parameters
            imratio = height/width
            plt.imshow(image) #Plotting the image
            plt.title(f'{title} on {date}, bands: r=B12, g=B11, b=B09')
            plt.xlabel(sorted_file_names[n])
            if not os.path.exists('images'):
                os.mkdir('images')
            plt.tight_layout()
            plt.savefig(f'images/{date}_image.png')
            plt.clf()
            print('Could not plot NBR/dNBR, not enough bands')
               
        else:
            NBR = np.zeros((height,width))    
            B12 = np.zeros((height,width))
            B11 = np.zeros((height,width))
            B09 = np.zeros((height,width))
            B08 = np.zeros((height,width))
            for i in range(height):
                for j in range(width):
                    B12[i][j] = data[width*height*0 + width*i+j] #updating band data for each of the 4 bands
                    B11[i][j] = data[width*height*1 + width*i+j]
                    B09[i][j] = data[width*height*2 + width*i+j]
                    B08[i][j] = data[width*height*3 + width*i+j]
            NBR = (B12-B08)/(B12+B08)      
            band1 = scale(B12) #scaling bands for plotting
            band2 = scale(B11)
            band3 = scale(B09)
            date  = extract_date(sorted_file_names[n])
            print(date)
            image = np.stack([band1,band2,band3], axis=2) #creating 3D matrix for RGB plot
        
            plt.figure(figsize=(15,15)) #setting figure parameters
            imratio = height/width
            plt.imshow(image) #Plotting the image
            plt.title(f'{title} on {date}, bands: r=B12, g=B11, b=B09')
            plt.xlabel(sorted_file_names[n])
            if not os.path.exists('images'):
                os.mkdir('images')
            plt.tight_layout()
            plt.savefig(f'images/{date}_image.png')
            plt.clf()
            
            '''
            plt.imshow(NBR, cmap='Greys') #Plotting the NBR
            plt.title(f'NBR of {title} on {date}')
            plt.colorbar(fraction=0.04525*imratio)     
            if not os.path.exists('NBR'):
                os.mkdir('NBR')
            plt.tight_layout()
            plt.savefig(f'NBR/{date}_{sorted_file_names[n]}.png')
            plt.clf()
        
            #Plotting the dNBR for all frames but the first
            if n == 0:
                start_NBR = NBR
            else:
                dNBR = start_NBR - NBR        
                plt.imshow(dNBR, cmap='Greys')
                plt.title(f'dNBR of {title} on {date}')
                plt.colorbar(fraction=0.04525*imratio)     
                if not os.path.exists('dNBR'):
                    os.mkdir('dNBR')
                plt.tight_layout()
                plt.savefig(f'dNBR/{date}_{sorted_file_names[n]}.png') 
                plt.clf()
            '''
from misc import exist, read_hdr, read_float, hdr_fn, read_binary
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors


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
    dNBR = preNBR - postNBR
    date  = end_frame.split('_')[2].split('T')[0]
    return dNBR

def class_plot(start_file, end_file): 
    '''
    Plots the BARC 256 burn severity of the provided start and end file and saves it as a png
    >>> class_plot('S2B_MSIL1C_20210626T185919_N0300_R013_T10UFB_20210626T211041.bin', 'S2A_MSIL1C_20210907T190911_N0301_R056_T10UFB_20210902T225534.bin')
    '''
    dnbr = dNBR(start_file,end_file)
    scaled_dNBR = (dnbr*1000+275)/5 #scalling dNBR
    class_plot = np.zeros((len(scaled_dNBR),len(scaled_dNBR[0])))
    for i in range(len(scaled_dNBR)): #making classifications
        for j in range(len(scaled_dNBR[0])):
            if scaled_dNBR[i][j] < 76:
                class_plot[i][j] = 0
            elif 76 <= scaled_dNBR[i][j] < 110:
                class_plot[i][j] = 1
            elif 110 <= scaled_dNBR[i][j] < 187:
                class_plot[i][j] = 2
            else:
                class_plot[i][j] = 3
                
    start = start_file.split('/')[-1] #splitting files for file names
    end = end_file.split('/')[-1]
    start_date  = start.split('_')[2].split('T')[0]
    end_date = end.split('_')[2].split('T')[0]
    
    cmap = matplotlib.colors.ListedColormap(['green','yellow','orange','red'])   #plotting
    imratio = len(scaled_dNBR)/len(scaled_dNBR[0])   
    plt.figure(figsize=(15,15))       
    plt.imshow(class_plot,cmap=cmap)
    plt.title(f'BARC 256 burn severity, start date:{start_date}, end date:{end_date}')
    plt.xlabel(f'start file:{start}, end file:{end}')
    plt.colorbar(fraction=0.04525*imratio)
    plt.tight_layout()
    plt.savefig(f'{end}_BARC_classification.png')
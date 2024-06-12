from misc import exist, read_hdr, read_float, hdr_fn, read_binary, extract_date
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import os


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
    nbrswir = (B11-B12-0.02)/(B11+B12+0.1)
    date  = file_name.split('_')[2].split('T')[0]
    '''
    plt.figure(figsize=(15,15))
    plt.imshow(NBR, cmap='Greys')
    plt.title(f'NBR of Sparks Lake fire on {date}')
    plt.tight_layout()
    plt.colorbar()
    '''
    return [B12,B11,B09,B08,NBR,height,width,nbrswir]
            
            
def dNBR(start_frame, end_frame):
    '''
    Takes the start and end binary files and returns the dNRB.
    >>> dNBR('S2B_MSIL1C_20210626T185919_N0300_R013_T10UFB_20210626T211041.bin', 'S2A_MSIL1C_20210907T190911_N0301_R056_T10UFB_20210902T225534.bin')
    '''
    predata = NBR(start_frame)
    postdata = NBR(end_frame)
    preNBR = predata[4]
    postNBR = postdata[4]
    preswir = predata[7]
    postswir = postdata[7]
    dNBR = preNBR - postNBR
    dNBRSWIR = preswir - postswir
    
    for i in range(len(dNBR)):
        for j in range(len(dNBR[0])):
            if predata[0][i][j] <= 100 or dNBRSWIR[i][j] <= 0.1:
                dNBR[i][j] = 0
            else:
                continue;
    
    date  = end_frame.split('_')[2].split('T')[0]
    #plt.colorbar()
    #plt.show()

    return dNBR

def class_plot(dNBR, start_date='Not given', end_date='Not given'): 
    '''
    Plots the BARC 256 burn severity of the provided start and end file and saves it as a png
    >>> class_plot('S2B_MSIL1C_20210626T185919_N0300_R013_T10UFB_20210626T211041.bin', 'S2A_MSIL1C_20210907T190911_N0301_R056_T10UFB_20210902T225534.bin')
    '''
    
    scaled_dNBR = (dNBR*1000+275)/5 #scalling dNBR
    class_plot = np.zeros((len(scaled_dNBR),len(scaled_dNBR[0])))
    un_tot = 0
    low_tot = 0
    med_tot = 0
    high_tot = 0
    for i in range(len(scaled_dNBR)): #making classifications
        for j in range(len(scaled_dNBR[0])):
            if scaled_dNBR[i][j] < 76:
                class_plot[i][j] = 0
                un_tot += 1
            elif 76 <= scaled_dNBR[i][j] < 110:
                class_plot[i][j] = 1
                low_tot += 1
            elif 110 <= scaled_dNBR[i][j] < 187:
                class_plot[i][j] = 2
                med_tot += 1
            else:
                class_plot[i][j] = 3
                high_tot += 1
                
    #start = sorted_file_names[0].split('/')[-1] #splitting files for file names
    #end = sorted_file_names[k].split('/')[-1]
    #start_date  = start.split('_')[2].split('T')[0]
    #end_date = end.split('_')[2].split('T')[0]
    #calculating percentages of each class
    tot = un_tot+low_tot+med_tot+high_tot
    un_per = round(100*un_tot/tot,1)
    low_per = round(100*low_tot/tot,1)
    med_per = round(100*med_tot/tot,1)
    high_per = round(100*high_tot/tot,1)
    

    '''
    cmap = matplotlib.colors.ListedColormap(['green','yellow','orange','red'])   #plotting
    plt.figure(figsize=(15,15))
    plt.imshow(class_plot,cmap=cmap)
    plt.title(f'BARC 256 burn severity, start date:{start_date}, end date:{end_date}')
    plt.scatter(np.nan,np.nan,marker='s',s=100,label=f'Unburned {un_per}%',color='green')
    plt.scatter(np.nan,np.nan,marker='s',s=100,label=f'Low {low_per}%' ,color='yellow')
    plt.scatter(np.nan,np.nan,marker='s',s=100,label=f'Medium {med_per}%',color='orange')
    plt.scatter(np.nan,np.nan,marker='s',s=100,label=f'High {high_per}%',color='red')
    plt.legend(fontsize="20")
    #plt.show()
    plt.tight_layout()
    plt.savefig(f'{end_date}_BARC_classification.png')
    '''
    return class_plot

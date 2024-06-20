from misc import exist, read_hdr, read_float, hdr_fn, read_binary, extract_date, write_binary, write_hdr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import os

def nbr_full(file_name):
    """
    Takes a binary file and returnes all bands as well as NBR,NBRSWIR and NVDI
    """
    vals = read_binary(file_name) 
    data = vals[3]
    width = vals[0]
    height = vals[1]
    band_names = ['B1','B2','B3','B4','B5','B6','B7','B8A','B08','B09','B11','B12']
    for b in band_names:
        exec(f"{b} = np.zeros(({height}, {width}))", globals())
        
    for i in range(height):
        for j in range(width):
            B12[i][j] = data[width*height*11 + width*i+j]
            B11[i][j] = data[width*height*10 + width*i+j]
            B09[i][j] = data[width*height*9 + width*i+j]
            B08[i][j] = data[width*height*8 + width*i+j]
            B8A[i][j] = data[width*height*7 + width*i+j]
            B7[i][j] = data[width*height*6 + width*i+j]
            B6[i][j] = data[width*height*5 + width*i+j]
            B5[i][j] = data[width*height*4 + width*i+j]
            B4[i][j] = data[width*height*3 + width*i+j]
            B3[i][j] = data[width*height*2 + width*i+j]
            B2[i][j] = data[width*height*1 + width*i+j]
            B1[i][j] = data[width*height*0 + width*i+j]

    NBR = (B08-B12)/(B08+B12)#calculating NBR
    NDVI = (B08 - B4)/(B08 + B4)#calculating NDVI
    
    nbrswir = (B11-B12-0.02)/(B11+B12+0.1)
    date  = file_name.split('_')[2].split('T')[0]
    '''
    plt.figure(figsize=(15,15))
    plt.imshow(NDVI, cmap='Greys')
    plt.title(f'NBR of Sparks Lake fire on {date}')
    plt.tight_layout()
    plt.colorbar()
    '''
    return [B1,B2,B3,B4,B5,B6,B7,B8A,B08,B09,B11,B12,NBR,NDVI,nbrswir, height,width]
            

def NBR(file_name):
    '''
    Takes binary file and returns the band values as well as the NBR.
    >>> NBR('S2A_MSIL1C_20210902T190911_N0301_R056_T10UFB_20210902T225534.bin')
    '''
    vals = read_binary(file_name) 
    data = vals[3]
    width = vals[0]
    height = vals[1]
    band_names = ['B08','B09','B11','B12']
    for b in band_names:
        exec(f"{b} = np.zeros(({height}, {width}))", globals())
        
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
    plt.imshow(NDVI, cmap='Greys')
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
    dNBR = preNBR - postNBR #calculating dNBR
    rdnbr = dNBR/(np.sqrt(abs(preNBR))) #calculating RdNBR
    dNBRSWIR = preswir - postswir # calculating dNBRSWIR
    
    #removing water and some noise
    for i in range(len(dNBR)):
        for j in range(len(dNBR[0])):
            if predata[0][i][j] <= 100 or rdnbr[i][j] < 0 or dNBRSWIR[i][j] < 0.1:
                dNBR[i][j] = 0
            else:
                continue;

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
    
    #calculating percentages           
    tot = un_tot+low_tot+med_tot+high_tot
    un_per = round(100*un_tot/tot,1)
    low_per = round(100*low_tot/tot,1)
    med_per = round(100*med_tot/tot,1)
    high_per = round(100*high_tot/tot,1)
    
    #write_binary(class_plot,'BARC_sparks.bin')
    #write_hdr('BARC_sparks.hdr', len(class_plot[0]), len(class_plot), 1)
    #plotting
    end_date_good = end_date.split('_')[0]
    cmap = matplotlib.colors.ListedColormap(['green','yellow','orange','red'])   #plotting
    plt.figure(figsize=(15,15))
    plt.imshow(class_plot,vmin=0,vmax=3,cmap=cmap)
    plt.title(f'BARC 256 burn severity, start date:{start_date}, end date:{end_date_good}')
    plt.scatter(np.nan,np.nan,marker='s',s=100,label=f'Unburned {un_per}%',color='green')
    plt.scatter(np.nan,np.nan,marker='s',s=100,label=f'Low {low_per}%' ,color='yellow')
    plt.scatter(np.nan,np.nan,marker='s',s=100,label=f'Medium {med_per}%',color='orange')
    plt.scatter(np.nan,np.nan,marker='s',s=100,label=f'High {high_per}%',color='red')
    plt.legend(fontsize="20")
    #plt.show()
    plt.tight_layout()
    plt.savefig(f'{end_date}_BARC_classification.png')

    return class_plot

'''
files = os.listdir('/Volumes/Lexar/L2_T10VEL/bins')
file_list = []
for n in range(len(files)):
    if files[n].split('.')[-1] == 'bin':
        file_list.append(files[n])
    else:
        continue;

sorted_file_names = sorted(file_list, key=extract_date)

start_file = sorted_file_names[1]
start_date = start_file.split('_')[2].split('T')[0]
for file in sorted_file_names[2:]:
    dnbr = dNBR(f'/Volumes/Lexar/L2_T10VEL/bins/{start_file}',f'/Volumes/Lexar/L2_T10VEL/bins/{file}')
    end_date = file.split('_')[2].split('T')[0]
    class_plot(dnbr,start_date,f'{end_date}_L2')
'''
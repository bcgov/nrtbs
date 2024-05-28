
from sklearn.linear_model import LinearRegression 
from dNBR import dNBR, NBR
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


filenames = ['S2B_MSIL1C_20210626T185919_N0300_R013_T10UFB_20210626T211041.bin','S2B_MSIL1C_20210629T190919_N0300_R056_T10UFB_20210629T212050.bin','S2A_MSIL1C_20210701T185921_N0301_R013_T10UFB_20210701T223921.bin','S2B_MSIL1C_20210709T190919_N0301_R056_T10UFB_20210709T224644.bin','S2A_MSIL1C_20210714T190921_N0301_R056_T10UFB_20210714T225634.bin','S2B_MSIL1C_20210719T190919_N0301_R056_T10UFB_20210719T212141.bin','S2A_MSIL1C_20210724T190921_N0301_R056_T10UFB_20210724T230122.bin','S2B_MSIL1C_20210726T185919_N0301_R013_T10UFB_20210726T211239.bin','S2B_MSIL1C_20210729T190919_N0301_R056_T10UFB_20210729T212314.bin','S2A_MSIL1C_20210803T190921_N0301_R056_T10UFB_20210803T224926.bin','S2B_MSIL1C_20210805T185919_N0301_R013_T10UFB_20210805T211134.bin','S2A_MSIL1C_20210813T190921_N0301_R056_T10UFB_20210813T224901.bin','S2A_MSIL1C_20210902T190911_N0301_R056_T10UFB_20210902T225534.bin','S2B_MSIL1C_20210907T190929_N0301_R056_T10UFB_20210907T224046.bin']


def model(stop_index, filenames): 
    '''
    Using a list of raster files this function models the dNBR of a given fire using linear regression and 4 parameters. The function plots both an error plot of the predicted vs observed final dNBR and the predicted dNBR. It also returns the fits score.
    '''
    if stop_index < 0 or stop_index >= len(filenames): err("bad index")  
    dnbr = dNBR(f'raster_data/small/{filenames[0]}', f'raster_data/small/{filenames[-1]}')  # dependent variable: compare start and end dates
    #nbr = NBR(f'raster_data/small/{filenames[-1]}')[4]
    
    params = []
    for i in range(stop_index + 1):  
        params += NBR(f'raster_data/small/{filenames[i]}')
 
    X = []
    Y = []
    height = 549
    width = 549
    for i in range(height):
        for j in range(width):
            x = [params[k][i][j] for k in range(len(params))]
            y = dnbr[i][j]
            #print(x)
            if not np.isnan(x).any():
                X += [x]
                Y += [y]     
            else:
                X += [[0 for k in range(len(params))]]
                Y += [0]

    reg = LinearRegression().fit(X, Y)
    pred = reg.predict(X)
    data = np.zeros((height,width))
    for n in range(len(pred)): #going through the prediction list to plot the predicted dNBR
        i = n // width
        j = n % height
        data[i][j] = pred[n]
    err = dnbr - data #error 
    plt.imshow(err,cmap='Greys') 
    plt.show()
    plt.imshow(data,cmap='Greys')
    plt.colorbar()
    plt.show()
    score = reg.score(X, Y)
    print(score) 
 
 
for i in range(len(filenames)):
    model(i, filenames) 


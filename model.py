
from sklearn.linear_model import LinearRegression 
from sklearn.neighbors import KNeighborsRegressor
from dNBR import dNBR, NBR
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

filenames = ['S2B_MSIL1C_20210626T185919_N0300_R013_T10UFB_20210626T211041.bin','S2B_MSIL1C_20210629T190919_N0300_R056_T10UFB_20210629T212050.bin','S2A_MSIL1C_20210701T185921_N0301_R013_T10UFB_20210701T223921.bin','S2B_MSIL1C_20210709T190919_N0301_R056_T10UFB_20210709T224644.bin','S2A_MSIL1C_20210714T190921_N0301_R056_T10UFB_20210714T225634.bin','S2B_MSIL1C_20210719T190919_N0301_R056_T10UFB_20210719T212141.bin','S2A_MSIL1C_20210724T190921_N0301_R056_T10UFB_20210724T230122.bin','S2B_MSIL1C_20210726T185919_N0301_R013_T10UFB_20210726T211239.bin','S2B_MSIL1C_20210729T190919_N0301_R056_T10UFB_20210729T212314.bin','S2A_MSIL1C_20210803T190921_N0301_R056_T10UFB_20210803T224926.bin','S2B_MSIL1C_20210805T185919_N0301_R013_T10UFB_20210805T211134.bin','S2A_MSIL1C_20210813T190921_N0301_R056_T10UFB_20210813T224901.bin','S2A_MSIL1C_20210902T190911_N0301_R056_T10UFB_20210902T225534.bin','S2B_MSIL1C_20210907T190929_N0301_R056_T10UFB_20210907T224046.bin']


def NBRmodel(stop_index, filenames, model_type): 
    '''
    Using a list of raster files and a model type this function models the NBR of a given fire using linear regression and 4 parameters. The function plots both an error plot of the predicted vs observed final dNBR and the predicted NBR. It also returns the fits score.
    model types:
    'lin_reg' == Linear Regression
    'KN_reg' == K Neighbor Regressor
    
    '''
    if stop_index < 0 or stop_index >= len(filenames): err("bad index")  
    nbr = NBR(f'raster_data/small/{filenames[-1]}')[4]# dependent variable: compare start and end dates
    
    params = []
    for i in range(stop_index + 1):  
        params += NBR(f'raster_data/small/{filenames[i]}') #making a list of parameters 
 
    X = []
    Y = []
    height = 549
    width = 549
    for i in range(height): #making training and test data
        for j in range(width):
            x = [params[k][i][j] for k in range(len(params))]
            y = nbr[i][j]
            if not np.isnan(x).any():
                X += [x]
                Y += [y]     
            else:
                X += [[0 for k in range(len(params))]]
                Y += [0]
    if model_type == 'linear_reg': #fitting linear regression
        reg = LinearRegression().fit(X, Y)
        pred = reg.predict(X)
        data = np.zeros((height,width))
        score = reg.score(X, Y)
    elif model_type == 'KN_reg': #fitting K Neighbor Regressor
        reg = KNeighborsRegressor().fit(X,Y)
        pred = reg.predict(X)
        data = np.zeros((height,width))
        score = reg.score(X, Y)        
    
    date = filenames[stop_index].split('_')[2].split('T')[0]
    for n in range(len(pred)): #going through the prediction list to plot the predicted NBR
        i = n // width
        j = n % height
        data[i][j] = pred[n]
    err = nbr - data #error 
    
    plt.figure(figsize=(15,15)) #plotting
    
    plt.imshow(err,cmap='Greys')
    plt.colorbar(fraction=0.04525)
    plt.title(f'NBR error using stop date {date}, using {model_type}. Score: {score}')
    if not os.path.exists('NBR_model_error'):
        os.mkdir('NBR_model_error') 
    plt.tight_layout()
    plt.savefig(f'NBR_model_error/{date}_{model_type}_{filenames[stop_index]}.png')
    plt.clf()
    
    plt.imshow(data,cmap='Greys')
    plt.colorbar(fraction=0.04525)
    plt.title(f'Predicted NBR using stop date {date}, using {model_type}. Score: {score}')
    if not os.path.exists('NBR_model'):
        os.mkdir('NBR_model')
    plt.tight_layout()
    plt.savefig(f'NBR_model/{date}_{model_type}_{filenames[stop_index]}.png')
    plt.clf()
 
    
def dNBRmodel(stop_index, filenames, model_type): 
    '''
    Using a list of raster files and a model type this function models the NBR of a given fire using linear regression and 4 parameters. The function plots both an error plot of the predicted vs observed final dNBR and the predicted NBR. It also returns the fits score.
    model types:
    'lin_reg' == linear regression
    'KN_reg' == K Neighbor Regressor
    '''
    if stop_index < 0 or stop_index >= len(filenames): err("bad index")  
    dnbr = dNBR(f'raster_data/small/{filenames[0]}', f'raster_data/small/{filenames[-1]}')  # dependent variable: compare start and end dates
    
    params = []
    for i in range(stop_index + 1):  
        params += NBR(f'raster_data/small/{filenames[i]}')#making a list of parameters 
 
    X = []
    Y = []
    height = 549
    width = 549
    for i in range(height): #making training and test data
        for j in range(width):
            x = [params[k][i][j] for k in range(len(params))]
            y = dnbr[i][j]
            if not np.isnan(x).any():
                X += [x]
                Y += [y]     
            else:
                X += [[0 for k in range(len(params))]]
                Y += [0]

    if model_type == 'linear_reg': #fitting linear regression
        reg = LinearRegression().fit(X, Y)
        pred = reg.predict(X)
        data = np.zeros((height,width))
        score = reg.score(X, Y)    
    elif model_type == 'KN_reg': #fitting K Neighbor Regressor
        reg = KNeighborsRegressor().fit(X,Y)
        pred = reg.predict(X)
        data = np.zeros((height,width))
        score = reg.score(X, Y) 
    
    date = filenames[stop_index].split('_')[2].split('T')[0]
    for n in range(len(pred)): #going through the prediction list to plot the predicted dNBR
        i = n // width
        j = n % height
        data[i][j] = pred[n]
    err = dnbr - data #error 
    test = dNBR(f'raster_data/small/{filenames[0]}',f'raster_data/small/{filenames[stop_index]}')
    
    
    plt.figure(figsize=(15,15)) #plotting
    
    plt.imshow(err,cmap='Greys')
    plt.colorbar(fraction=0.04525)
    plt.title(f'dNBR error using stop date {date}, using {model_type}. Score: {score}')
    if not os.path.exists('dNBR_model_error'):
        os.mkdir('dNBR_model_error') 
    plt.tight_layout()
    plt.savefig(f'dNBR_model_error/{date}_{model_type}_{filenames[stop_index]}.png')
    plt.clf()
    
    plt.imshow(data,cmap='Greys')
    plt.colorbar(fraction=0.04525)
    plt.title(f'Predicted dNBR using stop date {date}, using {model_type}. Score: {score}')
    if not os.path.exists('dNBR_model'):
        os.mkdir('dNBR_model')
    plt.tight_layout()
    plt.savefig(f'dNBR_model/{date}_{model_type}_{filenames[stop_index]}.png')
    plt.clf()

for i in range(len(filenames)):
    NBRmodel(i, filenames,'KN_reg')
    dNBRmodel(i,filenames,'KN_reg')

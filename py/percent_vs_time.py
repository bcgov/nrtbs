'''
Takes a file directory containing a composite sequence and plots the percent of data in the frame vs date of the frame.
'''
from misc import extract_date, read_binary
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

def extract_data_percent(file_dir):
    '''
    extracts and plots data percentage vs time
    '''
    #reading directory and sorting bin files
    files = os.listdir(file_dir)
    file_list = []
    for n in range(len(files)):
        if files[n].split('.')[-1] == 'bin':
            file_list.append(files[n])
        else:
            continue
    sorted_file_names = sorted(file_list, key=extract_date) 

    #calculating percent data for each frame
    percent_data = []
    dates = []
    ticks = []
    i = 0
    for file in sorted_file_names:
        data = read_binary(f'{file_dir}/{file}')[3]
        nans = sum(math.isnan(x) for x in data)
        percent_data.append(100 - 100*nans/len(data))
        dates.append(extract_date(file))
        if percent_data[-1] >= 93:
            break
        print(percent_data[-1])
        if i % 10 == 0: 
            ticks.append(extract_date(file))
        i += 1

    #plotting
    plt.figure(figsize=(15,15))
    plt.title('Percent data vs time of composite image sequence')
    plt.xlabel('Date')
    plt.ylabel('% data')
    plt.xticks(rotation=45)
    plt.plot(dates, percent_data)
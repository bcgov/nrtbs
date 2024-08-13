'''
donwloads sentinel data, extracts cloudfree swir nir bands, choses most recent avaialbe pixle, and merges frames (if necesary) for the given fire and date range
$python3 get_composite.py G90267 
$python3 get_composite.py 20240630 G90267 
$python3 get_composite.py N51117 N51069 N51210 N51103
$python3 get_composite.py 20240810 N51117 N51069 N51210 N51103
'''
from percent_vs_time import extract_data_percent
from misc import run, args, extract_date
from check_tile_id import check_tile_id
from cut_coords import plot_image_with_rectangle
from plot import plot
import os
import geopandas as gpd
from datetime import datetime, timedelta
from dnbr import time_series

def get_composite_image(fire_num, end_date=None):
    '''
    Takes a fire number as well as a tile ID and downloads an MRAP timesires composite
    '''
    #changing single fire numbers to list and naming multi fire scene
    if type(fire_num) == list:
        fire_name = f'{fire_num[0]}_complex'
        fire_nums = fire_num
    else:
        print(fire_num)
        fire_name = fire_num
        fire_nums = [fire_num]
    
    #taking end date as today none defined
    if end_date == None:
        end_date = datetime.today().date()
        str_end_date_comps = str(end_date).split('-')
        str_end_date = ''
        for comp in str_end_date_comps:
            str_end_date += comp
    else:
        str_end_date = end_date
    
    #getting the ignition date for fires and taking the smallest
    fire_perims_path = '../shape_files/prot_current_fire_points.shp'
    fire_perims = gpd.read_file(fire_perims_path)
    fire_perims = fire_perims.to_crs(epsg=4326)
    fire_num_perim = fire_perims[fire_perims['FIRE_NUM'].isin(fire_nums)]
    ignt_dates = [datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S').date() for date in  fire_num_perim.IGNITN_DT]
    fire_start_date = min(ignt_dates)
    start_date = fire_start_date - timedelta(weeks=3)

    #changing date format to string for sync_daterange script
    str_start_date_comps = str(start_date).split('-')
    str_start_date = ''
    for comp in str_start_date_comps:
        str_start_date += comp

    tiles = check_tile_id(fire_num) #checking tiles
    tile_str = ''
    for tile in tiles:
        tile_str += f' {tile}'
    
    sync_string = f'python3 sync_daterange_gid_zip.py {str_start_date} {str_end_date}' + tile_str #defining sync string
    run(sync_string) #running download script
    run('python3 sentinel2_extract_cloudfree_swir_nir.py') #running cloudfree extraction
    run('python3 sentinel2_mrap.py') #running MRAP script
    if len(tiles) > 1:
        run(f'python3 sentinel2_mrap_merge.py {fire_name}') #running merge script if necesary 

    #renaming directory and moving non MRAP frames
    else:
        os.rename(f'L2_{tiles[0]}', fire_name)
        os.mkdir(f'{fire_name}/{fire_name}_cloudfree')
        run(f'mv {fire_name}/*cloudfree.bin {fire_name}/{fire_name}_cloudfree')
        run(f'mv {fire_name}/*cloudfree.hdr* {fire_name}/{fire_name}_cloudfree')
    
    #getting list of files for cutting
    files = [x.strip() for x in os.popen(f'ls -1 {fire_name}/*.bin').readlines()] 
    files.sort()
    cut_data = plot_image_with_rectangle(files[-1]) #prompt user for cut coords
    run(f'python3 cut.py {fire_name} {int(cut_data[0])} {int(cut_data[1])} {int(cut_data[2])} {int(cut_data[3])}')

    #reading through files to find nearest date to start date
    files = os.listdir(f'{fire_name}_cut')
    date_list = []
    for n in range(len(files)):
        if files[n].split('.')[-1] == 'bin':
            date_list.append(extract_date(files[n]))
        else:
            continue
    date_list = sorted(date_list)
    for i in range(len(date_list)):
        if datetime.strptime(date_list[i], '%Y%m%d').date() >= (fire_start_date - timedelta(days=1)):
            barc_start = date_list[i-1]
            break

    extract_data_percent(f'{fire_name}_cut',barc_start) #plotting the data percent vs time for frames
    plot(f'{fire_name}_cut', fire_name) #plotting image, NBR, dNBR time series
    time_series(f'{fire_name}_cut', int(barc_start), f'{fire_name}_barcs') #plotting BARC time series
    
if __name__ == "__main__":

    if len(args[1]) == 8: #runs with specified end date if one is provided
        get_composite_image(args[2:], args[1])
    
    else: #runs with end date set to current date
        get_composite_image(args[1:])

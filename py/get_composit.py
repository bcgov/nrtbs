import numpy as np

from misc import run, args
from check_tile_id import check_tile_id
from cut_coords import plot_image_with_rectangle
from plot import plot
from dnbr import time_series
import os

def get_composit_image(fire_num, start_date, end_date):
    '''
    Takes a fire number as well as a tile ID and downloads an MRAP timesires composit
    '''
    tiles = check_tile_id(fire_num) #checking tiles
    tile_str = ''
    for tile in tiles:
        tile_str += f' {tile}'
    # sync_string = f'python3 sync_daterange_gid_zip.py {start_date} {end_date}' + tile_str
    # run(sync_string) #running download script
    # run('python3 sentinel2_extract_cloudfree_swir_nir.py') #running cloudfree extraction
    # run('python3 sentinel2_mrap.py') #running MRAP script
    if len(tiles) > 1:
        run(f'python3 sentinel2_mrap_merge.py {fire_num}') #running merge script if necesary 
    files = [x.strip() for x in os.popen(f'ls -1 {fire_num}/*.bin').readlines()] #sorting list of merged images
    files.sort()
    cut_data = plot_image_with_rectangle(files[-1])
    run(f'python3 cut.py {fire_num} {int(cut_data[0])} {int(cut_data[1])} {int(cut_data[2])} {int(cut_data[3])}')
    plot(f'{fire_num}_cut', fire_num)
    print('Run dnbr.py time_composit to produce BARC plots')
    
if __name__ == "__main__":
    get_composit_image(args[1],args[2],args[3])
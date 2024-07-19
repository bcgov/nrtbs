import numpy as np

from misc import run, args
from check_tile_id import check_tile_id
import os

def get_composit_image(fire_num, start_date, end_date):
    tiles = check_tile_id(fire_num)
    tile_str = ''
    for tile in tiles:
        tile_str += f' {tile}'
    sync_string = f'python3.12 ~/Documents/nrtbs/py/sync_daterange_gid_zip.py {start_date} {end_date}' + tile_str
    run(sync_string)
    run('python3.12 ~/Documents/nrtbs/py/sentinel2_extract_cloudfree_swir_nir.py')
    run('python3.12 ~/Documents/nrtbs/py/sentinel2_mrap.py')
    run(f'python3.12 ~/Documents/nrtbs/py/sentinel2_mrap_merge.py {fire_num}')
    
    
if __name__ == "__main__":
    get_composit_image(args[1],args[2],args[3])
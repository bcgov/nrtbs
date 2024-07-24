import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
from misc import run, args

fire_perims_path = '../shape_files/prot_current_fire_polys.shp'
tile_path = '../shape_files/Sentinel_BC_Tiles.shp'
def check_tile_id(fire_num):
    '''
    Checks which tiles a fire numbers perimeter is in, for downloading
    '''
    run('python3 get_perimeters.py')
    fire_perims_path = '../shape_files/prot_current_fire_polys.shp'
    #reading files 
    fire_perims = gpd.read_file(fire_perims_path)
    fire_perims = fire_perims.to_crs(epsg=4326)
    fire_num_perim = fire_perims[fire_perims['FIRE_NUM'] == fire_num]
    fire_geom = fire_num_perim.geometry.iloc[0]
    tile_id = gpd.read_file(tile_path)
    tile_id = tile_id.to_crs(epsg=4326)
    
    #checking which tiles perimeter is in 
    containing = tile_id[tile_id.geometry.intersects(fire_geom)]
    
    #saving tile names
    tile_names = []
    for name in containing['Name']:
        if name != np.nan:
            tile_names.append(f'T{name}')
    
    #plotting tiles to check if all are needed
    fig, ax = plt.subplots()
    i = 0
    colors = ['blue', 'green', 'purple', 'orange', 'brown', 'pink', 'gray']
    for idx, section in containing.iterrows():
        containing.loc[[idx]].plot(ax=ax,edgecolor='black', color=colors[i])
        ax.scatter(np.nan, np.nan, color=colors[i], marker='s', s=60,label=f'T{section["Name"]}')
        i += 1
        if i > 6:
            i = 0
    fire_num_perim.plot(ax=ax,edgecolor = 'black',color='red')
    ax.set_title(f'{fire_num} in Sentinel2 tiles', fontsize=14)
    ax.legend(fontsize=14)
    plt.show()
    return tile_names

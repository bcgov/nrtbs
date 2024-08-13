'''
Automatically calculates the cut cordinates given the fire perimeters geodatabase and a header file and returns a list of the start x, start y, width, and height
>>> auto_coords(fire_num_perim, 'N51117_complex/S2A_MSIL2A_20240729T183921_N0511_R070_T11UMR_20240730T023050_cloudfree.bin_MRAP.hdr')
[2928, 2690, 956, 2246]
'''
import geopandas as gpd
import re
from pyproj import Proj, Transformer
import matplotlib.pyplot as plt

def gdf_coords(gdf):
    '''
    Calculates the bounds of the fire perimeter
    '''
    gdf = gdf.to_crs(epsg=3005)
    bounds = gdf.total_bounds
    minx, miny, maxx, maxy = bounds
    return [maxx, maxy, minx, miny]


def extract_map_info(hdr_file_path):
    # Read the ENVI header file
    with open(hdr_file_path, 'r') as file:
        lines = file.readlines()

    # Initialize variables to hold map info values
    map_info = {
        "projection": None,
        "ulx": None,  # Upper-left X coordinate
        "uly": None,  # Upper-left Y coordinate
        "pixel_size_x": None,
        "pixel_size_y": None,
        "zone": None,
        "hemisphere": None,
        "datum": None
    }

    # Extract map info line
    map_info_line = None
    for line in lines:
        if 'samples' in line.lower():
            samples = int(line.strip().split(' ')[-1])
        elif 'lines' in line.lower():
            lines = int(line.strip().split(' ')[-1])
        elif 'map info' in line.lower():
            map_info_line = line.strip()
            break

    if map_info_line:
        # Extract values from map_info line
        map_info_values = re.findall(r'\{([^}]*)\}', map_info_line)
        if map_info_values:
            values = map_info_values[0].split(',')
            if len(values) >= 9:
                map_info["projection"] = values[0].strip()
                map_info["ulx"] = float(values[3].strip())
                map_info["uly"] = float(values[4].strip())
                map_info["pixel_size_x"] = float(values[5].strip())
                map_info["pixel_size_y"] = float(values[6].strip())
                map_info["zone"] = values[7].strip()
                map_info["hemisphere"] = values[8].strip()
                map_info["datum"] = values[9].strip()

    return [map_info, samples, lines]
    
def utm_to_latlon(utm_easting, utm_northing, zone_number, hemisphere):
    # Define the UTM projection
    proj_utm = Proj(f"+proj=utm +zone={zone_number} +{'north' if hemisphere.lower() == 'north' else 'south'} +datum=WGS84")
    
    # Define the EPSG:3005 projection (NAD83 / BC Albers)
    proj_epsg3005 = Proj("epsg:3005")
    
    # Transform UTM to latitude and longitude
    transformer = Transformer.from_proj(proj_utm, proj_epsg3005, always_xy=True)
    
    # Transform UTM coordinates to EPSG:3005
    x, y = transformer.transform(utm_easting, utm_northing)
    return x, y

def auto_coords(gdf,hdr_file):
    '''
    Calculates cut coords
    '''
    #getting data
    data = extract_map_info(hdr_file)
    map_info = data[0]
    samples = data[1]
    lines = data[2]

    #defining upper left and bottom right corners of header file
    ulx = map_info["ulx"]
    uly = map_info["uly"]
    brx = ulx + samples * float(map_info['pixel_size_x'])
    bry = uly - lines * float(map_info['pixel_size_y']) 

    #converting to epsg 3005
    x_top, y_top = utm_to_latlon(ulx, uly, map_info["zone"], map_info["hemisphere"])
    x_bot, y_bot = utm_to_latlon(brx, bry, map_info["zone"], map_info["hemisphere"])

    #calculating the scaling factor from pixle to epsg 3005
    x_con = lines/(x_bot - x_top)
    y_con = samples/(y_bot - y_top)

    shape_coords = gdf_coords(gdf) #getting fire perimeter epsg 3005 coords

    #calculating cut coordinates
    top_x = (shape_coords[2] - x_top) * x_con
    top_y = (shape_coords[1] - y_top) * y_con
    bot_x = (shape_coords[0] - x_top) * x_con
    bot_y = (shape_coords[3] - y_top) * y_con
    width = bot_x-top_x
    height = bot_y - top_y

    return[int(top_x-200), int(top_y-200), int(width+200), int(height+200)] #returning cut coords with buffer
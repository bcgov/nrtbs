'''
# Automatically calculates the cut cordinates given the fire perimeters geodatabase and a header file and returns a list of the start x, start y, width, and height
# >>> auto_coords(fire_num_perim, 'N51117_complex/S2A_MSIL2A_20240729T183921_N0511_R070_T11UMR_20240730T023050_cloudfree.bin_MRAP.hdr')
# [2928, 2690, 956, 2246]
# '''
# import geopandas as gpd
# import re
# from pyproj import Proj, Transformer
# import matplotlib.pyplot as plt

# def gdf_coords(gdf):
#     '''
#     Calculates the bounds of the fire perimeter
#     '''
#     gdf = gdf.to_crs(epsg=3005)
#     bounds = gdf.total_bounds
#     minx, miny, maxx, maxy = bounds
#     return [maxx, maxy, minx, miny]


# def extract_map_info(hdr_file_path):
#     # Read the ENVI header file
#     with open(hdr_file_path, 'r') as file:
#         lines = file.readlines()

#     # Initialize variables to hold map info values
#     map_info = {
#         "projection": None,
#         "ulx": None,  # Upper-left X coordinate
#         "uly": None,  # Upper-left Y coordinate
#         "pixel_size_x": None,
#         "pixel_size_y": None,
#         "zone": None,
#         "hemisphere": None,
#         "datum": None
#     }

#     # Extract map info line
#     map_info_line = None
#     projection_line = None
#     for line in lines:
#         if 'samples' in line.lower():
#             samples = int(line.strip().split(' ')[-1])
#         elif 'lines' in line.lower():
#             lines = int(line.strip().split(' ')[-1])
#         elif 'map info' in line.lower():
#             map_info_line = line.strip()
#         elif 'projection info' in line.lower():
#             projection_line  = line.strip()
#             break

#     if map_info_line:
#         # Extract values from map_info line
#         map_info_values = re.findall(r'\{([^}]*)\}', map_info_line)
#         if projection_line:
#             projection_values = re.findall(r'\{([^}]*)\}', projection_line)
#             map_values = map_info_values[0].split(',')
#             proj_vals = projection_values[0].split(',')

#             map_info["projection"] = "utm"
#             map_info["ulx"] = float(map_values[3].strip())
#             map_info["uly"] = float(map_values[4].strip())
#             map_info["pixel_size_x"] = float(map_values[5].strip())
#             map_info["pixel_size_y"] = float(map_values[6].strip())
#             map_info["zone"] = 10
#             map_info["hemisphere"] = 'North'
#             map_info["datum"] = 'WGS84'

#         else:
#             values = map_info_values[0].split(',')
#             if len(values) >= 9:
#                 map_info["projection"] = values[0].strip()
#                 map_info["ulx"] = float(values[3].strip())
#                 map_info["uly"] = float(values[4].strip())
#                 map_info["pixel_size_x"] = float(values[5].strip())
#                 map_info["pixel_size_y"] = float(values[6].strip())
#                 map_info["zone"] = values[7].strip()
#                 map_info["hemisphere"] = values[8].strip()
#                 map_info["datum"] = values[9].strip()

#     return [map_info, samples, lines]
    
# def utm_to_3005(utm_easting, utm_northing, zone_number, hemisphere):
#     # Define the UTM projection
#     proj_utm = Proj(f"+proj=utm +zone={zone_number} +{'north' if hemisphere.lower() == 'north' else 'south'} +datum=WGS84")

    
#     # Define the EPSG:3005 projection (NAD83 / BC Albers)
#     proj_epsg3005 = Proj("epsg:3005")
    
#     # Transform UTM to latitude and longitude
#     transformer = Transformer.from_proj(proj_utm, proj_epsg3005, always_xy=True)
    
#     # Transform UTM coordinates to EPSG:3005
#     x, y = transformer.transform(utm_easting, utm_northing)
#     return x, y

# def auto_coords(fire_num,hdr_file):
#     '''
#     Calculates cut coords
#     '''
#     fire_perims = gpd.read_file('../shape_files/prot_current_fire_polys.shp')
#     fire_num_perims = fire_perims[fire_perims['FIRE_NUM'].isin(fire_num)]

#     #getting data
#     data = extract_map_info(hdr_file)
#     map_info = data[0]
#     samples = data[1]
#     lines = data[2]

#     #defining upper left and bottom right corners of header file
#     ulx = map_info["ulx"]
#     uly = map_info["ulx"]
#     brx = ulx + samples * float(map_info['pixel_size_x'])
#     bry = uly - lines * float(map_info['pixel_size_y']) 

#     #converting to epsg 3005
#     x_top, y_top = utm_to_3005(ulx, uly, map_info["zone"], map_info["hemisphere"])
#     x_bot, y_bot = utm_to_3005(brx, bry, map_info["zone"], map_info["hemisphere"])

#     #calculating the scaling factor from pixle to epsg 3005
#     x_con = lines/(x_bot - x_top)
#     y_con = samples/(y_bot - y_top)

#     shape_coords = gdf_coords(fire_num_perims) #getting fire perimeter epsg 3005 coords

#     #calculating cut coordinates
#     top_x = (shape_coords[2] - x_top) * x_con
#     top_y = (shape_coords[1] - y_top) * y_con
#     bot_x = (shape_coords[0] - x_top) * x_con
#     bot_y = (shape_coords[3] - y_top) * y_con
#     width = bot_x-top_x
#     height = bot_y - top_y

#     return[int(top_x-200), int(top_y-200), int(width+200), int(height+200)] #returning cut coords with buffer

from osgeo import gdal
import geopandas as gpd
from pyproj import Proj, Transformer

def extract_map_info_from_gdal(file):
    """
    Extracts map info from a raster file using GDAL.

    Parameters:
    - hdr_file: Path to the raster header file.

    Returns:
    - A tuple with (geotransform, projection)
    """
    # Open the raster file using GDAL
    dataset = gdal.Open(file)
    
    # Extract the geotransform and projection
    geotransform = dataset.GetGeoTransform()
    projection = dataset.GetProjection()
    
    return geotransform, projection

def transform_coordinates(x, y, src_proj, tgt_proj):
    """
    Transform coordinates from source projection to target projection.

    Parameters:
    - x: Coordinate in the source projection (easting or longitude)
    - y: Coordinate in the source projection (northing or latitude)
    - src_proj: Source projection as a PROJ string or EPSG code
    - tgt_proj: Target projection as a PROJ string or EPSG code

    Returns:
    - x_transformed, y_transformed: Transformed coordinates in the target projection
    """
    # Define the source and target projections
    proj_src = Proj(src_proj)
    proj_tgt = Proj(tgt_proj)
    
    # Create a transformer for the transformation
    transformer = Transformer.from_proj(proj_src, proj_tgt, always_xy=True)
    
    # Transform coordinates
    x_transformed, y_transformed = transformer.transform(x, y)
    return x_transformed, y_transformed

def gdf_coords(gdf, target_crs):
    """
    Transforms the coordinates of the GeoDataFrame to the specified CRS.

    Parameters:
    - gdf: GeoDataFrame with the fire perimeter data.
    - target_crs: Target CRS as an EPSG code.

    Returns:
    - List of bounding coordinates in the target CRS.
    """
    gdf = gdf.to_crs(epsg=target_crs)
    bounds = gdf.total_bounds
    minx, miny, maxx, maxy = bounds
    return [maxx, maxy, minx, miny]

def auto_coords(fire_num, file):
    """
    Calculates cut coordinates for raster data and fire perimeters, transforming to a specified projection.

    Parameters:
    - fire_num: List of fire numbers to filter the perimeter data.
    - hdr_file: Path to the raster header file.
    - target_proj: Target projection as a PROJ string or EPSG code

    Returns:
    - List of cut coordinates with a buffer.
    """
    target_proj = 'epsg:3005'
    # Load fire perimeter data
    fire_perims = gpd.read_file('../shape_files/prot_current_fire_polys.shp')
    fire_num_perims = fire_perims[fire_perims['FIRE_NUM'].isin(fire_num)]

    # Extract map info from GDAL
    geotransform, projection = extract_map_info_from_gdal(file)
    print(projection)
    # Define the corners using the geotransform
    ulx = geotransform[0]
    uly = geotransform[3]
    pixel_size_x = geotransform[1]
    pixel_size_y = geotransform[5]
    
    # Calculate bottom right corner
    samples = geotransform[1]  # Number of columns
    lines = geotransform[5]    # Number of rows
    brx = ulx - samples * abs(pixel_size_x)
    bry = uly + lines * abs(pixel_size_y)
    
    # Transform corners to the target projection
    x_top, y_top = transform_coordinates(ulx, uly, projection, target_proj)
    x_bot, y_bot = transform_coordinates(brx, bry, projection, target_proj)

    # Calculate scaling factors
    x_con = lines / (x_bot - x_top)
    y_con = samples / (y_bot - y_top)

    # Transform fire perimeter coordinates
    shape_coords = gdf_coords(fire_num_perims, int(target_proj.split(':')[-1]))

    # Calculate cut coordinates
    top_x = (shape_coords[2] - x_top) * x_con
    top_y = (shape_coords[1] - y_top) * y_con
    bot_x = (shape_coords[0] - x_top) * x_con
    bot_y = (shape_coords[3] - y_top) * y_con
    width = bot_x - top_x
    height = bot_y - top_y

    return [int(top_x - 200), int(top_y - 200), int(width + 400), int(height + 400)]  # Returning cut coordinates with buffer

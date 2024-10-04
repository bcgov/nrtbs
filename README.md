# nrtbs (Near-Real-Time Burned Severity)
Application: **NRT "same-day" burned severity (automatic)**

* uses MRAP (Most Recent Available Pixel) "cloud-free" image compositing
* Access to ESA Sentinel-2 data via NRCAN NRT Sentinel products mirror on AWS-S3 (thanks ESA and NRCAN) 
 
## To run
```
git clone git@github.com:bcgov/nrtbs.git
cd nrtbs
python3 py/get_composite [FIRE_NUMBER] 
```
where [FIRE_NUMBER] is a 6-character BC wildfire "fire number" (a letter followed by 5 digits), for example:
```
python3 py/get_composite.py G90267
```
for the 2024 Parker Lake wildfire, affecting Fort Nelson (BC). 
* Start and end dates will be automatically generated based on fire ignition dates unless manual end date is given
* Automatic trimming to fire AOI
* Results will be output into a FIRE_NUMBER_barcs folder
## Notes:
Can add flag ```--no_update_listing``` to skip refreshing the index of all available Sentinel-2 data. Also a ```--skip_data_download``` is available for re-running without downloading the initial .zip format data again (e.g. if there are storage limitations, can use this to re-run after deleting all zip files but keeping intermediary products)
e.g.:
```
python3 py/get_composite.py G90267 --no_update_listing
```
## Dependencies
* Windows: first [please click here for instructions to install WSL prompt](https://learn.microsoft.com/en-us/windows/wsl/install) no admin privileges required in Windows
* Ubuntu Linux
In both cases, the following commands are needed before running the application
```
python3 -m pip install numpy matplotlib pandas rasterio geopandas
sudo apt install gdal-bin libgdal-dev python3-gdal
```
* Also compatible with MacOS (use brew install instead of sudo apt install) 

### Test procedure:
Rolling up the setup and invocation, to get started (assuming you have WSL installed) here is the available test procedure:
```
python3 -m pip install numpy matplotlib pandas rasterio geopandas
sudo apt install gdal-bin libgdal-dev
git clone git@github.com:bcgov/nrtbs.git
cd nrtbs
python3 py/get_composite.py 20240601 G90267
```

# Background / references
* [Sterling's original work instructions](doc/TASK.md)
* https://burnseverity.cr.usgs.gov/ravg/background-products-applications
* https://towardsdatascience.com/t-sne-clearly-explained-d84c537f53a
* https://github.com/SashaNasonova/burnSeverity/blob/main/burnsev_gee.py
* https://github.com/SashaNasonova/burnSeverity/blob/main/BurnSeverityMapping.ipynb

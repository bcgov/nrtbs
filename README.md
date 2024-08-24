# nrtbs (Near-Real-Time Burned Severity)
Application: **NRT "same-day" burned severity (automatic)**

* uses MRAP (Most Recent Available Pixel) "cloud-free" image compositing
* Access to ESA Sentinel-2 data via NRCAN NRT Sentinel products mirror on AWS-S3 (thanks ESA and NRCAN) 
 
## Running
```
git clone git@github.com:bcgov/nrtbs.git
cd nrtbs
python3 get_composite [FIRE_NUMBER]  # where [FIRE_NUMBER] is a 6-character BC wildfire "fire number" (a letter followed by 5 digits) 
```
* Open code repository in terminal
* Call "$ python3 get_composite FIRE_NUMBER" for single fire or "$ python3 get_composite FIRE_NUMBER1 FIRE_NUMBER2 ..." for a fire complex'
* Start and end dates will be automatically generated based on fire ignition dates unless manual end date is given
* Automatic trimming to fire AOI
* Results will be output into a FIRE_NUMBER_barcs folder
## Dependencies
* Windows: first [please click here for instructions to install WSL prompt](https://learn.microsoft.com/en-us/windows/wsl/install) no admin privileges required in Windows
* Ubuntu Linux
In both cases, the following commands are needed before running the application
```
python3 -m pip install numpy matplotlib pandas rasterio geopandas
sudo apt install gdal-bin gdal-dev
```
* Also compatible with MacOS (use brew install instead of sudo apt install) 

# Background / references
* [Sterling's original work instructions](doc/TASK.md)
* https://burnseverity.cr.usgs.gov/ravg/background-products-applications
* https://towardsdatascience.com/t-sne-clearly-explained-d84c537f53a
* https://github.com/SashaNasonova/burnSeverity/blob/main/burnsev_gee.py
* https://github.com/SashaNasonova/burnSeverity/blob/main/BurnSeverityMapping.ipynb

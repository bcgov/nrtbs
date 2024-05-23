# nrtbs
NRT burned severity
## Data Engineering
* Have a look at p 1-2 of [CSRS abstracts](https://github.com/bcgov/wps-research/blob/master/doc/2024_csrs/2024_csrs_abstracts.pdf)
* Review general details of [Sentinel-2 mission](https://sentiwiki.copernicus.eu/web/s2-mission)
* Install google cloud sdk [install google cloud SDK](https://cloud.google.com/sdk/docs/install). Could borrow the script [here](https://github.com/bcgov/wps-research/blob/master/py/gcp/install_gcp.py) and update it to the latest versions (and to work on MacOS)
* Install QGis
* Familiarize with Sentinel-2 tiling grid [https://sentiwiki.copernicus.eu/web/s2-products](https://sentiwiki.copernicus.eu/web/s2-products) by opening in QGis. Can add an XYZ layer (e.g. OpenStreetMap) to see the grid's relation to some geographic features
* Note: the grid is also available in Shapefile, clipped to BC area [here](https://github.com/bcgov/wps-research/blob/master/py/sentinel2_bc_tiles_shp/Sentinel_BC_Tiles.shp)
* Write a python function (in a .py file) to download all Sentinel-2 data (from GCP) available, in a time window (yyyymmdd1, yyyymmdd2) for one grid location e.g. T10UFB is Kamloops. Hopefully could reuse some of: [this one](https://github.com/bcgov/wps-research/blob/master/py/gcp/update_tile.py)
* Review BC documents [here](https://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/forestry/stewardship/forest-analysis-inventory/data-management/news/burn_severity_mapping_summary_210823.pdf) and [here](https://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/forestry/stewardship/forest-analysis-inventory/data-management/news/wildfire_2023_burn_severity_and_high_resolution_imagery.pdf) (should be a similar document for 2022 as well)
* Verify this is the correct link and download a province-wide burned-severity dataset for 2021 [here](https://catalogue.data.gov.bc.ca/dataset/fire-burn-severity-historical). Open it in QGis : )  
* Determine if "pre" and "post" imagery dates (used to generate the product) are listed within the dataset
* Download 2021 fire perimeters from: [here](https://www.for.gov.bc.ca/ftp/HPR/external/!publish/Maps_and_Data/GoogleEarth/WMB_Fires/) in KML format
* Fire of interest: Sparks lake K21001. Note: pre/post dates used in BC Gov BS estimate: 20200729 / 20220902  
* Rasterize burned severity product 
## Modelling
* Fit a sequence of models: where the independent variable is a time-series of Sentinel-2 data (starting with a cloud-free pre-fire date, and ending with date "X") Where "X" is >= the pre-fire date, and "X" <= the post-fire date. The post-fire date is the first cloud-free date after the fire is declared "out" (should be available from national fire polygon database, if not [here](https://www.for.gov.bc.ca/ftp/HPR/external/!publish/Maps_and_Data/GoogleEarth/WMB_Fires/). Easier: can choose a post-fire date by inspection (some time late in the season when the fire has obviously stopped moving).      
* Two cases: dependent variable is 1) burned-severity class or 2) the dNBR.
* Want to understand the goodness of fit for the dependent variable, as "X" is varied (want to see how small we can make "X" and still get a good estimate).
* Methods: start with [Scikit-learn](https://scikit-learn.org/stable/) and find something that runs in a finite amount of time. Try a few models in scikit-learn at least, before moving to more complex neural-network models such as in Pytorch or Keras/[Tensorflow](https://developers.google.com/machine-learning/crash-course)
### Preliminaries
* Select data frames (betwee pre-fire and post-fire date) with some cloud cover threshold e.g. <= 7%
* Likely want to plot the "spectra" (one curve for each band, date on the X-axis) for a variety of points: unburned, and different burned severity classes to get an idea of how the values change. Could write a script that does this using matplotlib. Can add coordinates for some manually selected points (of various classes) at the top of the file.   
## To consider later
* As a future refinement, may likely need to run Sen2cor processor [here](https://step.esa.int/main/snap-supported-plugins/sen2cor/sen2cor-v2-11/) as a pre-processing step to exclude detected areas. Info available [here](https://sentiwiki.copernicus.eu/web/s2-processing#S2Processing-L2AAlgorithmsS2-Processing-L2A-Algorithmstrue) on S2 processing algorithms resulting in the available cloud mask accompanying Level-2 data (running sen2cor on Level-1 data results in Level-2 data) 
* It may eventually be necessary to improve cloud vs. smoke vs. fire classification to refine our results.
## Application-izing
When we have arrived at an acceptable method that we determine is operationally relevant for anticipating burned-severity (while the fire is still burning) we need to collect the steps into an "application" that can be re-run (for re-use, including validation over larger areas) 

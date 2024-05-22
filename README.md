# nrtbs
NRT burned severity

## Tasks
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
* Fire of interest: [white rock lake](https://en.wikipedia.org/wiki/White_Rock_Lake_fire)
* note: Sparks lake K21001 pre/post dates used in BC Gov BS estimate: 20200729 / 20220902  
* Rasterize burned severity product 

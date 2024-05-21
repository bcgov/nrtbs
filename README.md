# nrtbs
NRT burned severity

## Tasks
* Review general details of [Sentinel-2 mission](https://sentiwiki.copernicus.eu/web/s2-mission)
* Install google cloud sdk [install google cloud SDK](https://cloud.google.com/sdk/docs/install). Could borrow the script [here](https://github.com/bcgov/wps-research/blob/master/py/gcp/install_gcp.py) and update it to the latest versions (and to work on MacOS)
* Install QGis
* Familiarize with Sentinel-2 tiling grid [https://sentiwiki.copernicus.eu/web/s2-products](https://sentiwiki.copernicus.eu/web/s2-products) by opening in QGis. Can add an XYZ layer (e.g. OpenStreetMap) to see the grid's relation to some geographic features
* Note: the grid is also available in Shapefile, clipped to BC area [here](https://github.com/bcgov/wps-research/blob/master/py/sentinel2_bc_tiles_shp/Sentinel_BC_Tiles.shp)
* Write a python function (in a .py file) to download all Sentinel-2 data (from GCP) available, in a time window (yyyymmdd1, yyyymmdd2) for one grid location e.g. T10UFB is Kamloops
* Review BC documents [here](https://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/forestry/stewardship/forest-analysis-inventory/data-management/news/burn_severity_mapping_summary_210823.pdf) and [here](https://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/forestry/stewardship/forest-analysis-inventory/data-management/news/wildfire_2023_burn_severity_and_high_resolution_imagery.pdf) (should be a similar document for 2022 as well)
* Verify this is the correct link and download a province-wide burned-severity dataset for 2021 (https://catalogue.data.gov.bc.ca/dataset/fire-burn-severity-historical)[here]. Open it in QGis : )  

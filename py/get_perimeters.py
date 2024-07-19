import datetime
import urllib.request
import shutil
import zipfile
import ssl
import certifi

'''
Downloads the current fire perimeters as a zip file
'''
# Create a timestamp for the backup filename
t = datetime.datetime.now().strftime("%Y%m%d%H%M")

# Define the filename and download path
fn = 'shape_files/prot_current_fire_polys.zip'
dl_path = 'https://pub.data.gov.bc.ca/datasets/cdfc2d7b-c046-4bf0-90ac-4897232619e1/' + fn

# Create an SSL context using certifi
context = ssl.create_default_context(cafile=certifi.where())

# Download the file using urllib with SSL context
with urllib.request.urlopen(dl_path, context=context) as response, open(fn, 'wb') as out_file:
    shutil.copyfileobj(response, out_file)

# Create a backup of the downloaded file with a timestamp
shutil.copyfile(fn, 'prot_current_fire_polys_' + t + '.zip')

# Extract the contents of the zip file
with zipfile.ZipFile(fn, 'r') as zip_ref:
    zip_ref.extractall()

print("Download and extraction complete.")

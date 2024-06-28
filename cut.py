'''20220814 subset image with GDAL, cleanup ENVI header
'''
from misc import run, err, exist, args
from envi import envi_header_cleanup, envi_header_copy_bandnames

if len(args) < 6:
    err('cut.py [src image] [gdal translate -srcwin parameter 1] [-srcwin param 2] [ -srcwin param 3] # cut image with GDAL and cleanup headers 20220814')

A, B, C, D = args[2: 6]
fn = args[1]

of = 'sub.bin'
#if exist(of): 
#    err('output file already exists: sub.bin')

run('gdal_translate -of ENVI -ot Float32 -srcwin ' + (' '.join([A, B, C, D])) +
    ' ' + fn +  # input file
    ' sub.bin')  # output file

envi_header_copy_bandnames(['',fn[:-4] + '.hdr', 'sub.hdr'])
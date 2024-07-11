'''20220814 subset image with GDAL, cleanup ENVI header
'''
from misc import run, err, exist, args
from envi import envi_header_cleanup, envi_header_copy_bandnames
import os

if len(args) < 6:
    err('cut.py [src image] [gdal translate -srcwin parameter 1] [-srcwin param 2] [ -srcwin param 3] # cut image with GDAL and cleanup headers 20220814')
    
A, B, C, D = args[2: 6]
fn = args[1]

def cut(fn, A, B, C, D):

    out_fn = f'{fn.strip('.bin')}_cut.bin'
    out_fn_hdr = f'{fn.strip('.bin')}_cut.hdr'
    print(f' out file name: !!!!!! {fn}')

    run(f'gdal_translate -of ENVI -ot Float32 -srcwin { (' '.join([A, B, C, D]))} {fn} {out_fn}')  # output file

    envi_header_copy_bandnames(['',fn[:-4] + '.hdr', out_fn_hdr])

if __name__ == "__main__":
    
    files = []
    if args[1][-4:] == '.bin':
        files += [args[1]]
        
    else:
        files += [x.strip() for x in os.popen("ls -1 " + args[1] + os.path.sep + "*.bin").readlines()]
        
    for f in files:
        print(f)
        cut(f, A, B, C, D)
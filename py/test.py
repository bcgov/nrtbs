from misc import run
import os
from cut_coords import plot_image_with_rectangle

files = [x.strip() for x in os.popen(f'ls -1  G90267/*cut.bin').readlines()] #sorting list of merged images
files.sort()
cut_data = plot_image_with_rectangle(files[-1])
print(cut_data)
run(f'python3 cut.py G90267 {cut_data[0]} {cut_data[1]} {cut_data[2]} {cut_data[3]}')
from misc import extract_date
from plot import plot_image
import matplotlib.pyplot as plt

def extract_data_percent(file_dir):
    files = os.listdir(file_dir)
    file_list = []
    for n in range(len(files)):
        if files[n].split('.')[-1] == 'bin':
            file_list.append(files[n])
        else:
            continue
    

    sorted_file_names = sorted(file_list, key=extract_date)
    data = plot_image(sorted_file_names[-1])
    plt.imshow(data)
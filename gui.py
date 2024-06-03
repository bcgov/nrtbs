import matplotlib.pyplot as plt
from plot import plot
from dNBR import NBR


def gui(file_list, width):
   nbr =  NBR(file_list[-1])
   date  = file_list[-1].split('_')[2].split('T')[0]
   print(nbr[5])
   plt.figure(figsize=(15,15)) #setting figure parameters
   imratio = nbr[5]/nbr[6]
   plt.plot(nbr[4])
   plt.title(f'NBR of Sparks Lake fire on {date}')
   plt.colorbar(fraction=0.04525*imratio)
   plt.show()

'''     
ax = plt.gca()
fig = plt.gcf()
implot = ax.imshow(im)
'''

def onclick(event):
    if event.xdata != None and event.ydata != None:
        print(event.xdata, event.ydata)
cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()

filenames = ['S2B_MSIL1C_20210626T185919_N0300_R013_T10UFB_20210626T211041.bin','S2B_MSIL1C_20210629T190919_N0300_R056_T10UFB_20210629T212050.bin','S2A_MSIL1C_20210701T185921_N0301_R013_T10UFB_20210701T223921.bin','S2B_MSIL1C_20210709T190919_N0301_R056_T10UFB_20210709T224644.bin','S2A_MSIL1C_20210714T190921_N0301_R056_T10UFB_20210714T225634.bin','S2B_MSIL1C_20210719T190919_N0301_R056_T10UFB_20210719T212141.bin','S2A_MSIL1C_20210724T190921_N0301_R056_T10UFB_20210724T230122.bin','S2B_MSIL1C_20210726T185919_N0301_R013_T10UFB_20210726T211239.bin','S2B_MSIL1C_20210729T190919_N0301_R056_T10UFB_20210729T212314.bin','S2A_MSIL1C_20210803T190921_N0301_R056_T10UFB_20210803T224926.bin','S2B_MSIL1C_20210805T185919_N0301_R013_T10UFB_20210805T211134.bin','S2A_MSIL1C_20210813T190921_N0301_R056_T10UFB_20210813T224901.bin','S2A_MSIL1C_20210902T190911_N0301_R056_T10UFB_20210902T225534.bin','S2B_MSIL1C_20210907T190929_N0301_R056_T10UFB_20210907T224046.bin']

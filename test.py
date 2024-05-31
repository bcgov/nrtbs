import numpy as np
import matplotlib.pyplot as plt
import os
from operator import add, sub
import datetime
'''

band1 = np.zeros((20,20,3))
band1[1][1][1] = 5
print(band1)
x = np.zeros((20,20))
y = np.zeros((20,20))
z = np.zeros((20,20))

for i in range(20):
    for j in range(20):
        x[i][j] += i*j
        y[i][j] += 1
        z[i][j] += i+j
        
image = np.stack([z,y,x], axis=2)
plt.figure(figsize=(15,15))
plt.tight_layout()

plt.imshow(image)
plt.savefig('images/bah2.png')

im_ratio = len(x[0])/len(x[1])
print(im_ratio)
plt.imshow(x, cmap='hot', interpolation='nearest')
plt.colorbar(fraction=0.04525)
plt.tight_layout()
plt.savefig('abh.png')

plt.imshow(y, cmap='hot', interpolation='nearest')
#plt.colorbar(fraction=0.04525)
plt.tight_layout()
plt.savefig('abh2.png')


x = np.array([[1,2,3,4,5],[6,7,8,9,10]])
y = np.array([[1,2,3,4,5],[6,7,8,9,10]])

print(x+y)

'''
'''
nan = np.array([[np.nan,np.nan,np.nan],[1,2,3],[np.nan,np.nan,np.nan],[1,2,3]])
for n in nan:
    if np.nan in n[0][0]:
        print('Yayy')
'''
'''
        
X = []
Y = 12
X += [Y]
X += [15]
print(X)


params = [[1,2,3,4,5,5,6,7,8,9,0],[1,2,3,4,5,5,6,7,8,9,0],[1,2,3,4,5,5,6,7,8,9,0]]
x = [params[k][1] for k in range(len(params))]
print(5490//10)
'''
'''
x = True
if x:
    print(5)

print(np.std([1,2,3,4,5,6]))
'''
'''
x = datetime.datetime.strptime('20210626','%Y%m%d')
y = [1,2,3,4,5,6,7,8,np.nan]
print(np.nanstd(y))

z = ['x','y','z','t']
for el in z:
    el = 10
    
print(z[1])


band_list = {'b12':,'b11','b09','b08','nbr'}
for band in band_list:
    band = 10
    
print(band_list)
'''
'''
band_title = ['B12', 'B11', 'B09', 'B08', 'NBR']
for band in range(4):
    print(band_title[band])
    
'''
print(5%5)
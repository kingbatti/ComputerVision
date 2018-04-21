# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 15:40:51 2018

@author: Moritz Lahann
"""

import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
from skimage.io import imread, imsave


lenna = imread("./Lenna.png")


#Aufg. 1

#2. was ist mit zusammenfuegen gemeint?
lennar = lenna[:,:,0]
lennag = lenna[:,:,1]
lennab = lenna[:,:,2]

lenna_grey = lenna
for pixel_x in range(lenna.shape[0]):
    for pixel_y in range(lenna.shape[1]):
        lenna_grey[pixel_x][pixel_y] = (int(lennar[pixel_x][pixel_y]) +
                                        int(lennag[pixel_x][pixel_y]) +
                                        int(lennab[pixel_x][pixel_y]))/3
plt.imshow(lenna_grey, cmap='Greys_r')

#5. Alle Werte werden invertiert
lennainv = 255-lenna

#3. heller -> farbe staerker vorhanden
fig, ax = plt.subplots(2, 3)

ax[0,0].imshow(lennar, cmap='Greys_r')
ax[0,0].set_title('Rotkanal')

ax[0,1].imshow(lennag, cmap='Greys_r')
ax[0,1].set_title('Gruenkanal')

ax[0,2].imshow(lennab, cmap='Greys_r')

ax[0,2].set_title('Blaukanal')

ax[1,0].imshow(lennainv)

ax[1,0].set_title('RGB invertiert')

ax[1,1].imshow(lenna)
ax[1,1].set_title('Original')
plt.show(block=True)  # This command shows the plt-windows. Not necessary in all IDEs

#6. Achsen muessen ausgewaehlt werden
rgbmean = np.mean(lenna, axis=(0,1))
rgbstd = np.std(lenna, axis=(0,1))

#Aufg. 2

d = np.load('./trainingsDatenFarbe2.npz')
trImgs = d['data']
trLabels = d['labels']

valD = np.load('./validierungsDatenFarbe2.npz')
valImgs = valD['data']
valLabels = valD['labels'] 

def Aufg31Farbe():
    trMeans = []
    for count in range(trImgs.shape[0]):
        trMeans.append(np.mean(trImgs[count,:,:], axis = (0,1)))
    
    valMeans = []
    for count in range(valImgs.shape[0]):
        valMeans.append(np.mean(valImgs[count,:,:], axis = (0,1)))
        
    labels = []
    
    for count in range(len(valMeans)):
        dists = []    
        for i in range(len(trMeans)):
            dists.append(np.linalg.norm(trMeans[i]-valMeans[count]))
        labels.append(trLabels[dists.index(min(dists))])
    
    return labels  

print np.sum(valLabels==Aufg31Farbe())
print np.sum(valLabels==Aufg31Farbe()) / float(valImgs.shape[0]) * 100

#50% Genauigkeit, also deutlich besseres Ergebnis

#Aufg. 3

def Aufg32Farbe(bins):
    
    trHists = []
    
    for count in range(trImgs.shape[0]):
        img = trImgs[count,:,:,:]
        rotKanal = img[:,:,0]
        gruenKanal = img[:,:,1]
        blauKanal = img [:,:,2]
        trHists.append((makeHist(rotKanal, bins), makeHist(blauKanal, bins), makeHist(gruenKanal, bins)))
    
    valHists = []
    
    for count in range(valImgs.shape[0]):
        img = valImgs[count,:,:,:]
        rotKanal = img[:,:,0]
        gruenKanal = img[:,:,1]
        blauKanal = img [:,:,2]
        valHists.append((makeHist(rotKanal, bins), makeHist(blauKanal, bins), makeHist(gruenKanal, bins)))
    
    labels = []
    
    for count in range(len(valHists)):
        dists = []    
        for i in range(len(trHists)):
            dists.append(np.linalg.norm(np.asarray(trHists[i])-np.asarray(valHists[count])))
        labels.append(trLabels[dists.index(min(dists))])
        
    return labels

def makeHist(img, nrBins):
    return np.histogram(img, bins = nrBins)[0]

#Das kann ein bisschen dauern je nach PC
def optimalBins():
    percentages = []
    for i in range(1,256):
        percentages.append(Aufg32Farbe(i))
    return max(percentages), percentages.index(max(percentages))

print optimalBins()
print np.sum(valLabels==Aufg32Farbe(219))
print np.sum(valLabels==Aufg32Farbe(219)) / float(valImgs.shape[0]) * 100

#Optimales Ergebnis is 56.666...% mit 219 bins
#Wenn ich mich richtig erinnere nicht viel besser als mit Graustufenhistogrammen
    

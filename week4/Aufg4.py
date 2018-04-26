# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 16:24:44 2018

@author: 6peters
"""

import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
import glob
from skimage import transform

val_imgs = glob.glob('./ComputerVision-master/week4/haribo1/hariboVal/*.png')
tr_imgs = glob.glob('./ComputerVision-master/week4/haribo1/hariboTrain/*.png')

val_labels = [x.split('/')[-1].split('.')[0].split('_')[0] for x in val_imgs]
tr_labels = [x.split('/')[-1].split('.')[0].split('_')[0] for x in tr_imgs]
    
#general helper functions
def load_imgs():
    for i,img in enumerate(val_imgs):
        val_imgs[i] = imread(img)
    for i,img in enumerate(tr_imgs):
        tr_imgs[i] = imread(img)
        
        
def compare_correct(labels):
    count = 0
    for i,label in enumerate(labels):
        if val_labels[i] == label:
            count += 1
    return count
        
        
#task functions
def classify_means():
    val_means = []
    tr_means = []
    for img in val_imgs:
        val_means.append(np.mean(img, axis=(0, 1)))
    for img in tr_imgs:
        tr_means.append(np.mean(img, axis=(0, 1)))
    return val_means, tr_means
    

def compare_means():
    means = classify_means()
    val_means = means[0]
    tr_means = means[1]
    labels = []
    
    for count in range(len(val_means)):
        dists = []
        for i in range(len(tr_means)):
            dists.append(np.linalg.norm(tr_means[i] - val_means[count]))
        labels.append(tr_labels[np.argmin(dists)])

    return labels
    
    
def classify_3dhists():
    val_hists = []
    tr_hists = []
    for img in val_imgs:
        img = img.reshape((img.shape[0]*img.shape[1],3))
        val_hists.append(np.histogramdd(img, bins = [8,8,8], range=((0,256),(0,256),(0,256)))[0])
    for img in tr_imgs:
        img = img.reshape((img.shape[0]*img.shape[1],3))
        tr_hists.append(np.histogramdd(img, bins = [8,8,8], range=((0,256),(0,256),(0,256)))[0])
    return val_hists, tr_hists
        
def compare_3dhists():
    hists = classify_3dhists()
    val_hists = hists[0]
    tr_hists = hists[1]
    labels = []
    
    for count in range(len(val_hists)):
        dists = []
        for i in range(len(tr_hists)):
            dists.append(np.linalg.norm(tr_hists[i] - val_hists[count]))
        labels.append(tr_labels[np.argmin(dists)])

    return labels      
    
    

if __name__ == '__main__':
    load_imgs()
    print val_labels
    print compare_means()
    print compare_correct(compare_means()), 'Labels were chosen correct'
    print compare_3dhists()
    print compare_correct(compare_3dhists()), 'Labels were chosen correct'
    
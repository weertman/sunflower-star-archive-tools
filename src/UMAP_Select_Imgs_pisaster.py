# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 16:43:35 2023

@author: wlwee
"""

#%%
import shutil
import umap
import glob
import os
import random
import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from tqdm import tqdm
import sklearn.cluster as cluster
from embedding_selector import embedding_selector as es

#%%

target_dim = (50,50)
ncomps = 25
nimgs = 500
nimgs_per_cluster = 1
nclusters = int(nimgs/nimgs_per_cluster)
if (nimgs / nimgs_per_cluster) * nimgs_per_cluster != nimgs:
    print('make sure; int(nimgs / nimgs_per_cluster) * nimgs_per_cluster == nimgs')

imgs_root_dir = r'C:/Users/wlwee/Documents/PycnoSurvey/DATA/iNat_PNW_Stars/Pisaster_ochraceus'
target_dir = os.path.join(imgs_root_dir, str(nimgs)+'_umap_selection_es')
if os.path.exists(target_dir) != True:
    os.mkdir(target_dir)

imgs = glob.glob(os.path.join(imgs_root_dir, '*', '*.jpg'))
imgs = [s for s in imgs if os.path.basename(target_dir) not in s]
imgs = [s for s in imgs if '0' != os.path.basename(os.path.dirname(s))]

imgs_target_dir = glob.glob(os.path.join(target_dir, '*.jpg'))
imgs = [s for s in imgs if s not in imgs_target_dir]

#%%

keep_imgs = es.use_embedding_selector_on_images(target_dir, imgs, target_number_of_images=nimgs, n_clusters=nclusters,
                                                 resize_save_imgs = False)















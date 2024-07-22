# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 12:29:25 2023

@author: wlwee
"""
#%%
import glob
import os
from PIL import Image
from tqdm import tqdm

#%%

img_ext = '.*'
data_dir = r'E:/StarStaringsCombToMakeSmall/CamaBeach/'
target_dir = os.path.join(os.path.dirname(data_dir), 'small')
if os.path.exists(target_dir) != True:
    os.mkdir(target_dir)
target_y_dim = 1000
path_imgs = glob.glob(os.path.join(data_dir, '*' + img_ext))


pbar = tqdm(total = len(path_imgs), position=0, leave=True)
for path_img in path_imgs:
    path_new_img = os.path.join(target_dir, os.path.basename(path_img))
    with Image.open(path_img) as img:
        size = img.size
        y = size[1]
        resize = target_y_dim/y
        n_dim = (int(size[0]*resize), target_y_dim)
        img_resize = img.resize(n_dim)
        img_resize.save(path_new_img)
    pbar.update(n=1)
pbar.close()
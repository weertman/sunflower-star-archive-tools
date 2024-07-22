# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 15:32:29 2023

@author: wlwee
"""

#%%
import rawpy
import imageio

import matplotlib.pyplot as plt

import cv2

import os
import glob

from datetime import datetime

from tqdm import tqdm
#%%
target_dir = r'E:\D7100_BRIDGET_IMGS'

path_imgs = glob.glob(r'F:\DCIM\101D7100\*.NEF')

name_ext = ''

#### Add get ctime code ####

show_imgs = True
img_ext = '.png'

existing_imgs = glob.glob(os.path.join(target_dir, '*' + img_ext))
existing_imgs_short = [os.path.basename(s).split('_')[2:] for s in existing_imgs]
existing_imgs_short = [s[0] + '_' + s[1] for s in existing_imgs_short]
existing_imgs_short = [s.split('.')[0] for s in existing_imgs_short]

exists_already = {}
for path_img in path_imgs:
    if os.path.basename(path_img).split('.')[0] in existing_imgs_short:
        exists_already[path_img] = 1
    else:
        exists_already[path_img] = 0

#%%

pbar = tqdm(total = len(path_imgs), position=0, leave=True)
for i, path_img in enumerate(path_imgs[0:]):
    c_time = str(os.path.getmtime(path_img)).split('.')[0]
    
    new_path_img = os.path.join(target_dir, name_ext +'_' + c_time + '_' + os.path.basename(path_img).split('.')[0]+img_ext)

    exists = exists_already[path_img]
    
    if exists == 0:
        with rawpy.imread(path_img) as raw:
            rgb = raw.postprocess()
            if show_imgs == True:
                fig, (ax) = plt.subplots(1,1,figsize=(10,10))
                ax.imshow(rgb)
                ax.axis('off')
                ax.set_title(new_path_img)
                plt.show(fig)
                plt.close(fig)
            cv2.imwrite(new_path_img, cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))             
    pbar.update(n=1)
pbar.close()


# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 12:55:44 2023

@author: wlwee
"""

import os
import glob
import shutil
from tqdm import tqdm
import cv2

target_dir = r'E:\images_for_cvat\pws_ww'
path_images = glob.glob(os.path.join(r'E:\SunflowerStarSightings\PWS_2023_WW',
                                     '*', '*.png'))
path_images = path_images + glob.glob(os.path.join(r'E:\SunflowerStarSightings\PWS_2023_BW',
                                     '*', '*.png'))
dsize = (2007, 1508)
n = 0
pbar = tqdm(total = len(path_images), position=0, leave=True)
for path_image in path_images:
    if n % 50 == 0:
        target_sub_dir = os.path.join(target_dir, str(n))
        if os.path.exists(target_sub_dir) != True:
            os.mkdir(target_sub_dir)
    
    new_path_image = os.path.join(target_sub_dir, os.path.basename(path_image))
    if os.path.exists(new_path_image) != True:
        #shutil.copyfile(path_image, new_path_image)
        image = cv2.imread(path_image)
        image = cv2.resize(image, dsize)
        cv2.imwrite(new_path_image, image)

    pbar.update(n=1)
    n += 1
pbar.close()


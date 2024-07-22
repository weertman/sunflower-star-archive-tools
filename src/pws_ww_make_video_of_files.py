# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 12:46:25 2023

@author: wlwee
"""

import os
import glob
import cv2
import numpy as np
from tqdm import tqdm
from datetime import datetime

def get_epochtime_from_path_img (s):
    e = s.split('_')[1]
    e = int(e)
    return e

def convert_epoch_to_date(epoch_str):
    """Convert epoch time string to formatted date."""
    epoch_time = int(epoch_str)
    dt_object = datetime.fromtimestamp(epoch_time)
    return dt_object.strftime("%m/%d/%y %H:%M:%S")

def get_max_dimensions(image_paths, 
                       text_padding=50):
    max_width, max_height = 0, 0
    for path in tqdm(image_paths, desc="Fetching image sizes"):
        image = cv2.imread(path)
        if image is None:
            raise ValueError(f"Error reading image: {path}")
        height, width, _ = image.shape

        # Accommodate the text padding into the height
        height_with_text = height + text_padding
        if width > max_width:
            max_width = width
        if height_with_text > max_height:
            max_height = height_with_text

        del image

    return max_width, max_height

def process_images(
        image_paths, 
        max_width, 
        max_height, 
        text_padding=50, 
        output_path="output_video.avi", 
        font_scale=3, 
        font_thickness=3, 
        font_color=(255, 255, 255), 
        dir_name_pos=(30, 80), 
        img_name_offset=100
    ):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 1, (max_width, max_height))

    for path in tqdm(image_paths, desc="Processing images"):
        image = cv2.imread(path)
        
        # Extract directory name and format image name
        dir_name = os.path.basename(os.path.dirname(path))
        img_name_parts = os.path.basename(path).split('.')[0].split('_')
        img_name = convert_epoch_to_date(img_name_parts[1]) + ' ' + img_name_parts[2]

        # Add the text with padding
        height, width, _ = image.shape
        padded_img = cv2.copyMakeBorder(image, text_padding, 0, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        
        cv2.putText(padded_img, dir_name, dir_name_pos, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_color, font_thickness)
        img_name_pos = (dir_name_pos[0] + len(dir_name) * img_name_offset, dir_name_pos[1])
        cv2.putText(padded_img, img_name, img_name_pos, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_color, font_thickness)

        # Center the image
        height_with_text = height + text_padding
        top = (max_height - height_with_text) // 2
        bottom = max_height - height_with_text - top
        left = (max_width - width) // 2
        right = max_width - width - left
        
        centered_img = cv2.copyMakeBorder(padded_img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

        out.write(centered_img)

        del image
        del padded_img
        del centered_img

    out.release()

    out.release()

if __name__ == "__main__":
    
    text_padding=100
    
    # Sample image paths list
    image_paths = glob.glob(os.path.join(r'E:\SunflowerStarSightings\PWS_2023_WW', '*', '*.png'))[0:]
    image_paths = sorted(image_paths, key = get_epochtime_from_path_img)

    max_width, max_height = get_max_dimensions(image_paths, text_padding=text_padding)
    output_path = r'E:\SunflowerStarSightings\PWS_2023_WW.avi'
    process_images(image_paths, max_width, max_height, 
                   text_padding=text_padding, output_path=output_path)

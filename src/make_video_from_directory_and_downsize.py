# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 13:32:56 2023

@author: wlwee
"""

import os
import cv2
import numpy as np
from tqdm import tqdm
import datetime

def downsize_video(input_path, output_path, ratio=0.25):
    print('downsizing')
    # Open the video
    vid = cv2.VideoCapture(input_path)

    if not vid.isOpened():
        print("Error: Could not open video.")
        return

    # Get original video's width, height and fps
    original_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = vid.get(cv2.CAP_PROP_FPS)

    # Calculate the new resolution
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)

    # Define codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height))

    while True:
        ret, frame = vid.read()

        if not ret:
            break

        # Resize the frame
        resized_frame = cv2.resize(frame, (new_width, new_height))
        
        # Write the resized frame to the new video
        out.write(resized_frame)

    # Release everything when done
    vid.release()
    out.release()
    cv2.destroyAllWindows()

def create_video_from_images(directory_path, output_file="output_video.avi"):
    print(f'opening {directory_path}')
    # List all PNG files in the directory
    png_files = [f for f in os.listdir(directory_path) if f.endswith('.png')][0:]
    png_files.sort()  # Sort images if needed

    # Initialize max height and total width
    max_height = 0
    max_width = 0
    images = []

    # Determine max height and total width
    pbar = tqdm(total = len(png_files), position=0, leave=True)
    for png in png_files:
        # Extract the epoch timestamp from the filename
        epoch_time = int(png.split('_')[1])  # assuming the format is always like '_{epoch}_...'
        readable_time = datetime.datetime.utcfromtimestamp(epoch_time).strftime('%B %d, %Y')
    
        img = cv2.imread(os.path.join(directory_path, png), cv2.IMREAD_UNCHANGED)
    
        # Add the datetime text to the image
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 5
        font_thickness = 2
        color = (255, 255, 255)  # White color
    
        cv2.putText(img, 
                    readable_time, 
                    (10, 200),  # top left corner
                    font, 
                    font_scale, 
                    color, 
                    font_thickness, 
                    lineType=cv2.LINE_AA)
        h, w, _ = img.shape
        max_height = max(max_height, h)
        max_width = max(max_width, w)
        images.append(img)
        pbar.update(n=1)
    pbar.close()
    
    print(f'max_height = {max_height}')
    print(f'max_width = {max_width}')

    # Define the codec and create a VideoWriter object
    print(f'writing video to {output_file}')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_file, 
                          fourcc, 
                          1, 
                          (max_width, max_height))

    # Place each image on the canvas and write to video
    pbar = tqdm(total = len(images), position=0, leave=True)
    for img in images:
        h, w, _ = img.shape
        y_offset = (max_height - h) // 2
        x_offset = (max_width - w) // 2  # Added this line
        canvas = 0 * np.ones((max_height, max_width, 3), np.uint8)  # Create a white canvas
        canvas[y_offset:y_offset+h, x_offset:x_offset+w] = img[:, :]  # Adjusted this line
        out.write(canvas)
        pbar.update(n=1)
    pbar.close()

if __name__ == "__main__":
    dir_path = r'E:\star_cages'
    output_file = os.path.join(dir_path, 'starcages.avi')
    create_video_from_images(dir_path, output_file)
    output_file_downsize = os.path.join(dir_path, 'starcages_downsized.avi')
    downsize_video(output_file, output_file_downsize)

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 11:34:12 2023

@author: wlwee
"""

import os
from tqdm import tqdm

def create_folders(directory_path, start_folder=121, num_folders=20):
    # Ensure the directory exists
    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' does not exist!")
        return

    # Create folders with a progress bar
    for i in tqdm(range(start_folder, num_folders + start_folder), desc="Creating folders"):
        folder_name = str(i).zfill(4)  # Format to 4 digits, i.e., 0001, 0002, etc.
        folder_path = os.path.join(directory_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)  # Ensure the folder is created

    print(f"Created {num_folders} folders in '{directory_path}'")

if __name__ == "__main__":
    directory_path = r'E:\SunflowerStarSightings\PWS_2023_BW'
    create_folders(directory_path)
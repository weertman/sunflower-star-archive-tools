import os
import glob
import shutil

target_dir = r'E:\SunflowerStarArchive\PWS_2023'
src_dir_0 = r'E:\SunflowerStarArchive\PWS_2023_JU'
src_dir_1 = r'E:\SunflowerStarArchive\PWS_2023_WW'
src_dir_2 = r'E:\SunflowerStarArchive\PWS_2023_BW'
src_dirs = [src_dir_0, src_dir_1, src_dir_2]

## finds all individuals in the source directories
## these are the unique subfolder basenames
individuals = []
for src_dir in src_dirs:
    individuals += [os.path.basename(x) for x in glob.glob(src_dir + '/*')]

print('Found', len(individuals), 'individuals')
for individual in individuals:
    print(individual)

## create dataframe containing the paths to the images for each individual and which source directory they came from
## this will be used to copy the images to the target directory
import pandas as pd

img_ext = '.png'

individuals_long = []
individuals_img_paths_long = []
src_dirs_long = []

for individual in individuals:
    print('Processing individual:', individual)
    for src_dir in src_dirs:
        individual_dir = os.path.join(src_dir, individual)
        src_paths = glob.glob(os.path.join(individual_dir, '*' + img_ext))
        print(os.path.join(individual_dir, '*' + img_ext), 'Found', len(src_paths), 'images in', individual_dir, 'in', src_dir)
        for src_path in src_paths:
            individuals_long.append(individual)
            individuals_img_paths_long.append(src_path)
            src_dirs_long.append(os.path.basename(src_dir))

df = pd.DataFrame({'individual': individuals_long, 'img_path': individuals_img_paths_long, 'src_dir': src_dirs_long})
print(df.head())

from tqdm import tqdm

## copying over the files
for i, row in tqdm(df.iterrows()):
    individual = row['individual']
    img_path = row['img_path']
    src_dir = row['src_dir']
    new_individual_dir = os.path.join(target_dir, individual)
    if os.path.exists(new_individual_dir) != True:
        os.makedirs(new_individual_dir)
    new_src_dir = os.path.join(new_individual_dir, src_dir)
    if os.path.exists(new_src_dir) != True:
        os.makedirs(new_src_dir)
    new_img_path = os.path.join(new_src_dir, os.path.basename(img_path))
    if os.path.exists(new_img_path) != True:
        shutil.copy(img_path, new_img_path)
        print('Copied', img_path, 'to', new_img_path)
    else:
        print(new_img_path, 'already exists')
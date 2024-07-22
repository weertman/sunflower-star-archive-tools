import os
import glob
import shutil
from tqdm import tqdm

src_dir = r'C:\Users\wlwee\OneDrive\Desktop\lab_stars_pycno_deployment'
sub_dir_head = '8_29_2023_WW_PICS'

src_sub_dirs = glob.glob(os.path.join(src_dir, '*'))

print('Found', len(src_sub_dirs), 'subdirectories')

remove_old = True

for sub_dir in tqdm(src_sub_dirs):
    print('Processing', sub_dir)
    sub_sub_dir = os.path.join(sub_dir, sub_dir_head)
    if os.path.exists(sub_sub_dir) != True:
        os.makedirs(sub_sub_dir)

    path_imgs = glob.glob(os.path.join(sub_dir, '*.png'))
    new_path_imgs = [os.path.join(sub_sub_dir, os.path.basename(path_img)) for path_img in path_imgs]
    print('\tFound', len(path_imgs), 'images')

    for path_img, new_path_img in zip(path_imgs, new_path_imgs):
        if os.path.exists(new_path_img) != True:
            shutil.copy(path_img, new_path_img)
            print('\tCopied', path_img, 'to', new_path_img)
            if remove_old == True:
                os.remove(path_img)
                print('\tRemoved', path_img)
        else:
            print('\tAlready exists:', new_path_img)
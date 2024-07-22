
#%%

import os
import cv2
import urllib.request
from skimage import io
import pandas as pd

#%%

path_csv = r'..\DATA\iNat_PNW_Stars\observations-288863.csv'
df = pd.read_csv(path_csv)
#%%
species = sorted(df['scientific_name'].unique())

#%%

nimgs_per_sub_dir = 100

# Create a directory for each species
for specie in species[:]:
    path_specie = os.path.join(os.path.dirname(path_csv), specie.replace(' ', '_'))
    if os.path.exists(path_specie) != True:
        os.mkdir(path_specie)

    dat = df[df['scientific_name'] == specie]
    dat = dat.reset_index(drop=True)
    # Create a subdirectory for each 100 images
    for i in range(0, len(dat), nimgs_per_sub_dir):
        path_sub_dir = os.path.join(path_specie, str(i))
        if os.path.exists(path_sub_dir) != True:
            os.mkdir(path_sub_dir)
        
        # Download the images
        for j in range(i, i+nimgs_per_sub_dir):
            if j < len(dat):
                obs_n = dat.loc[j, 'url'].split('/')[-1].split('.')[0]
                path_img = os.path.join(path_sub_dir, obs_n + '.jpg')
                if os.path.exists(path_img) != True:
                    urllib.request.urlretrieve(dat.loc[j, 'image_url'], path_img)
                    # io.imsave(path_img, io.imread(dat.loc[j, 'image_url']))
                    # img = cv2.imread(dat.loc[j, 'image_url'])
                    # cv2.imwrite(path_img, img)
                else:
                    print('Image already exists: ' + path_img)
            else:
                break

        subset = dat[i:i+nimgs_per_sub_dir]
        subset.to_csv(os.path.join(path_sub_dir, f'iNatObs.csv'), index=False)
        
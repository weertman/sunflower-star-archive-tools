
#%%
import os
import glob
from embedding_selector import embedding_selector as es

#%%

path_imgs = glob.glob(r'D:\Placozoa\data\dish_videos\*\*.JPG')
print(f'Number of images: {len(path_imgs)}')

target_dir = r'D:\PlacSeg\data\To_Be_Annotated_Images\2_21_2023_yolov8_training_imgs'
if os.path.exists(target_dir) != True:
    os.mkdir(target_dir)
print(target_dir)

#%%

keep_imgs = es.use_embedding_selector_on_images(target_dir, path_imgs, target_number_of_images=200,
                                                n_clusters=200, n_components_pca=200, n_components_umap=15,
                                                resize_save_imgs=True, target_dim=(640,640),
                                                n_neighbors=100, min_dist=0.01, metric='euclidean',)



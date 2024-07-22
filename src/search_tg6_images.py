import os
import glob
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
import shutil
from tqdm import tqdm
import matplotlib.pyplot as plt

def load_images_to_memory(root_path):
    images = []
    path_images = glob.glob(os.path.join(root_path, '*', '*.png'))
    print(f"Loading {len(path_images)} images to memory...")
    for path in tqdm(path_images):
        img = Image.open(path)
        images.append((img, path))
    return images

def find_closest_match(target_path, images,win_size=7, show=True):
    target_img = Image.open(target_path).convert('L')
    target_img_array = np.array(target_img)
    data_range = target_img_array.max() - target_img_array.min()
    print(f"Finding closest match for {os.path.basename(target_path)}...")
    print(f"Target image shape: {target_img_array.shape}")
    max_similarity = -1
    closest_match = None
    for img, img_path in tqdm(images, desc="Comparing images"):
        img = Image.open(img_path).convert('L')
        img_array = np.array(img)
        print(f"\tImage shape: {img_array.shape}")
        if img_array.shape == target_img_array.shape:
            similarity = ssim(target_img_array, img_array, multichannel=True, win_size=win_size, data_range=data_range)
            if similarity > max_similarity:
                max_similarity = similarity
                closest_match = img_path
                print(f"\t\tNew closest match found: {os.path.basename(closest_match)} with SSIM: {similarity}")
                if show and max_similarity > 0.6:
                    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
                    axs[0].imshow(target_img_array, cmap='gray')
                    axs[0].set_title("Target Image")
                    axs[0].set_xlabel(os.path.basename(target_path))
                    axs[0].axis('off')
                    axs[1].imshow(img_array, cmap='gray')
                    axs[1].set_title(f"Closest Match, SSIM: {similarity:.2f}")
                    ax[1].set_xlabel(os.path.basename(img_path))
                    axs[1].axis('off')
                    plt.show()
                    plt.close()
    return closest_match

def copy_closest_match(target_path, archive_path):
    images = load_images_to_memory(archive_path)
    closest_match = find_closest_match(target_path, images)
    if closest_match:
        target_folder = os.path.dirname(target_path)
        shutil.copy(closest_match, target_folder)
        print(f"Copied closest match {os.path.basename(closest_match)} to {target_folder}")
    else:
        print("No close match found.")

def main():
    archive = 'E:\TG6_IMGS_EXPORT'
    target = 'E:\SunflowerStarArchive\BROWN_ISLAND\DriftaRoni\8_9_2023\_1691617336_P8093731.png'

    copy_closest_match(target, archive)

if __name__ == "__main__":
    main()


from concurrent.futures import ProcessPoolExecutor, as_completed
import os
import multiprocessing
import os
import glob
import cv2
from PIL import Image
import rawpy
import time
from tqdm import tqdm
from datetime import datetime

def convert_image(image_path, target_path, image_type):
    if image_type == 'ORF':
        with rawpy.imread(image_path) as raw:
            rgb = raw.postprocess(use_camera_wb=True, output_bps=16, no_auto_bright=True)
            cv2.imwrite(target_path, cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
    elif image_type == 'JPG':
        with Image.open(image_path) as img:
            img.save(target_path, "PNG", compress_level=0)

def process_images_in_block(image_block, current_subfolder):
    for path_img in image_block:
        image_type = 'ORF' if '.ORF' in path_img.upper() else 'JPG'
        file_name = os.path.basename(path_img).split('.')[0] + '.png'
        new_path_img = os.path.join(current_subfolder, file_name)
        if os.path.exists(new_path_img) != True:
            convert_image(path_img, new_path_img, image_type)

def create_subfolder(target_dir, block_index, start_date, end_date):
    subfolder_name = f"{block_index}_{start_date}__{end_date}"
    subfolder_path = os.path.join(target_dir, subfolder_name)
    print(f"Creating subfolder: {subfolder_path}")
    os.makedirs(subfolder_path, exist_ok=True)
    return subfolder_path

def split_into_blocks(paths, block_size):
    for i in range(0, len(paths), block_size):
        yield paths[i:i + block_size]

def get_creation_date(path):
    # Change the format to "Month_Day_Year"
    return datetime.fromtimestamp(os.path.getctime(path)).strftime('%B_%d_%Y')

def main():
    source_dir = 'G:\\DCIM\\100OLYMP\\'
    target_dir = 'E:\\TG6_IMGS_EXPORT\\'
    block_size = 50

    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)

    path_imgs = glob.glob(source_dir + '*.ORF') + glob.glob(source_dir + '*.JPG')

    ## check current subdirs so that block_index can be updated
    existing_subfolders = glob.glob(os.path.join(target_dir, '*'))

    ## check all the subdirs for images that have already been processed
    path_imgs = [img for img in path_imgs if os.path.basename(img).split('.')[0] not in [os.path.basename(s).split('_')[-1] for s in existing_subfolders]]

    existing_subfolders = [os.path.basename(s) for s in existing_subfolders]
    existing_subfolders = [s.split('_')[0] for s in existing_subfolders]
    existing_subfolders = [int(s) for s in existing_subfolders]
    if len(existing_subfolders) > 0:
        starting_block_index = max(existing_subfolders)
    else:
        starting_block_index = 0

    path_imgs.sort(key=lambda x: os.path.getctime(x))

    image_blocks = list(split_into_blocks(path_imgs, block_size))

    # Define the number of processes
    num_processes = max(1, multiprocessing.cpu_count()-6)  # Ensure at least 1 process
    print(f"Using {num_processes} processes")

    start_time = time.time()  # Start timing

    futures = []
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        for block_index, image_block in enumerate(image_blocks):
            block_index += starting_block_index
            start_date = get_creation_date(image_block[0])
            end_date = get_creation_date(image_block[-1])
            current_subfolder = create_subfolder(target_dir, block_index + 1, start_date, end_date)
            future = executor.submit(process_images_in_block, image_block, current_subfolder)
            futures.append(future)

        # Wrap as_completed in tqdm for a progress bar
        for _ in tqdm(as_completed(futures), total=len(futures), desc="Processing Blocks"):
            # Progress bar updates automatically
            pass

    end_time = time.time()  # End timing
    print("All image blocks processed.")
    print(f"Total time taken: {end_time - start_time:.2f} seconds.")


if __name__ == '__main__':
    main()
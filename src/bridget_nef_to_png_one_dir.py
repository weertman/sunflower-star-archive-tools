import os
import glob
import cv2
import rawpy
import imageio
from tqdm import tqdm

src_dir = r'D:\pycno_pics_joey\pycno_post_deployment_pics'
dst_dir = os.path.join(src_dir, 'png')
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

path_nef_files = glob.glob(os.path.join(src_dir, '*.NEF'))

for path_nef_file in tqdm(path_nef_files):
    with rawpy.imread(path_nef_file) as raw:
        rgb = raw.postprocess(use_camera_wb=True)

    # Convert the RGB data to a format suitable for OpenCV (BGR)
    img = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    img_shape = img.shape

    # Check if the image is vertical and rotate if necessary
    if img.shape[0] > img.shape[1]:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    # Define the destination path for the PNG file
    base_name = os.path.basename(path_nef_file).split('.')[0]
    dst_path_png_file = os.path.join(dst_dir, base_name + '.png')

    # Save the processed image to the destination directory
    cv2.imwrite(dst_path_png_file, img)

    print(f'Processed {dst_path_png_file}, shape_before: {img_shape}, shape_after: {img.shape}')




import os
import shutil
import glob
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from pyzxing import BarCodeReader
import sys
import contextlib
from concurrent.futures import ThreadPoolExecutor, as_completed

# Context manager to suppress stderr
@contextlib.contextmanager
def suppress_stderr():
    stderr = sys.stderr
    sys.stderr = open(os.devnull, 'w')
    try:
        yield
    finally:
        sys.stderr.close()
        sys.stderr = stderr

def apply_augmentations(image):
    # Augmentation 1: Increase brightness
    bright_img = cv2.convertScaleAbs(image, alpha=1.2, beta=50)

    # Augmentation 2: Enhance contrast
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    contrast_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # Augmentation 3: Sharpen image
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharp_img = cv2.filter2D(image, -1, kernel)

    return [bright_img, contrast_img, sharp_img]

def get_central_qr_code_url_pyzbar(image):
    # Decode QR codes in the image
    qr_codes = decode(image)

    if not qr_codes:
        return None  # No QR codes found

    image_height, image_width, _ = image.shape

    # Function to calculate the distance from the center
    def distance_from_center(x, y):
        center_x = image_width / 2
        center_y = image_height / 2
        return np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

    # Find the most central QR code
    central_qr_code = min(qr_codes, key=lambda qr: distance_from_center(qr.rect.left + qr.rect.width / 2,
                                                                        qr.rect.top + qr.rect.height / 2))

    # Extract the URL from the central QR code
    qr_data = central_qr_code.data.decode('utf-8')

    return qr_data

def get_central_qr_code_url_zxing(image_path):
    reader = BarCodeReader()
    result = reader.decode(image_path)

    if not result or 'barcode_format' not in result:
        return None

    qr_codes = result['barcodes']

    if not qr_codes:
        return None  # No QR codes found

    image = cv2.imread(image_path)
    image_height, image_width, _ = image.shape

    # Function to calculate the distance from the center
    def distance_from_center(x, y, width, height):
        center_x = image_width / 2
        center_y = image_height / 2
        return np.sqrt((x + width / 2 - center_x) ** 2 + (y + height / 2 - center_y) ** 2)

    # Find the most central QR code
    central_qr_code = min(qr_codes, key=lambda qr: distance_from_center(qr['x'], qr['y'], qr['width'], qr['height']))

    return central_qr_code['raw']

def process_image(image_path):
    image = cv2.imread(image_path)

    if image is None:
        print(f"Failed to read {image_path}")
        return image_path, None

    # Try to find the QR code in the original image
    url = get_central_qr_code_url_pyzbar(image)

    # If no QR code is found, try augmentations
    if url is None:
        augmented_images = apply_augmentations(image)
        for aug_image in augmented_images:
            url = get_central_qr_code_url_pyzbar(aug_image)
            if url is not None:
                break

    if url is None:
        url = get_central_qr_code_url_zxing(image_path)

    return image_path, url

if __name__ == '__main__':
    # Test the function
    url_dir = os.path.join('..', '..', 'data', 'url_sort', 'june_11_2024_pizzahut')
    if not os.path.exists(url_dir):
        raise Exception('The directory does not exist')

    path_images = os.path.join(url_dir, '*.png')
    target_dir = os.path.join(url_dir, 'url_sort_v0')

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    else:
        shutil.rmtree(target_dir)
        os.makedirs(target_dir)

    qr_code_dict = {}
    with suppress_stderr():
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(process_image, image_path): image_path for image_path in glob.glob(path_images)}
            for future in as_completed(futures):
                image_path, url = future.result()
                if url is not None:
                    print(url)
                else:
                    print('No QR code found in', image_path)
                qr_code_dict[image_path] = url

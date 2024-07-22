import os
import glob
import cv2
import numpy as np
import torch
from ultralytics import YOLO
from tqdm import tqdm

## set cwd to the directory of this file
os.chdir(os.path.dirname(os.path.abspath(__file__)))
path_model = os.path.join('..', 'models', 'yolov8', 'Laboratory_StarSeg_Yolov8.pt')
#path_model = os.path.join('..', 'models', 'yolov8', 'sunflowerstarseg-4-20240402', 'train', 'weights', 'best.pt')
if os.path.exists(path_model):
    model = YOLO(path_model)
    print('Model found at', path_model)
    # Move the model to the appropriate device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print('Device:', device)
    model.to(device)
    #print('Model:', model)
else:
    print('Model not found at', path_model)
    raise FileNotFoundError

src_root_dir = r'C:\Users\wlwee\Downloads\TF_sampling_29August23\zion'
src_sub_dirs = glob.glob(os.path.join(src_root_dir, '*'))
print('Found', len(src_sub_dirs), 'src subdirectories')

dst_root_dir = r'C:\Users\wlwee\OneDrive\Desktop\lab_stars_pycno_deployment'
dst_sub_dirs = glob.glob(os.path.join(dst_root_dir, '*', '8_29_2023_WW_PICS'))
print('Found', len(dst_sub_dirs), 'dst subdirectories')

subsample_frames = 20
inference_batch_size = 32

for src_sub_dir in src_sub_dirs:
    src_sub_dir_base = os.path.basename(src_sub_dir)
    ## remove caps
    src_sub_dir_base = src_sub_dir_base.lower()
    ## check if the subdirectory exists in the destination subdirectories
    dst_sub_dir = [x for x in dst_sub_dirs if src_sub_dir_base == os.path.basename(os.path.dirname(x))]
    if len(dst_sub_dir) == 0:
        print(f'{src_sub_dir_base} not found in destination subdirectories')
    elif len(dst_sub_dir) > 1:
        print(f'Error! multiple matches found for {src_sub_dir_base}: {dst_sub_dir}')
        raise ValueError
    elif len(dst_sub_dir) == 1:
        dst_sub_dir = dst_sub_dir[0]
        print(f'src_sub_dir_base: {src_sub_dir_base}, dst_sub_dir: {dst_sub_dir}')

        path_src_videos = glob.glob(os.path.join(src_sub_dir, '*.mp4'))
        images = []
        ## grab an image every 40 frames
        for path_video in tqdm(path_src_videos):
            cap = cv2.VideoCapture(path_video)
            l = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            for i in range(0,l,subsample_frames):
                cap.set(1,i)
                ret, frame = cap.read()
                if ret:
                    frame = frame.astype(np.uint8)
                    images.append(frame)
                else:
                    print(f'Error reading frame {i} from {path_video}')
                    break
            cap.release()
        print(f'\tFound {len(images)} images in {path_src_videos}')
        for image_set in range(0, len(images), inference_batch_size):
            images_batch = images[image_set:image_set+inference_batch_size]
            results = model(images_batch, imgsz=640)
            for i, result in enumerate(results):
                image_path = os.path.join(dst_sub_dir, f'{image_set+i}__{src_sub_dir_base}.png')
                image = images_batch[i].copy()
                names = result.names  # Class names
                boxes = result.boxes  # Boxes object for bounding box outputs
                masks = result.masks  # Masks object for segmentation masks outputs

                if masks == None:
                    print(f'\t\t No starfish found in image {image_set+i}__{src_sub_dir_base}.png, skipping')
                    continue

                ## find index of largest mask
                max_area = 0
                max_index = 0
                for i, mask in enumerate(masks):
                    area = mask.data.cpu().numpy().sum()
                    if area > max_area:
                        max_area = area
                        max_index = i
                for i, key in enumerate(names.keys()):
                    name = names[key]
                    if name == 'Pycnopodia_helianthoides' and i == max_index:
                        box = boxes[i].xyxy.cpu().numpy()[0]
                        cropped_image = image[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
                        ## check if image is really dark
                        if np.mean(cropped_image) < 20:
                            print(f'\t\t Found dark image {image_set+i}__{src_sub_dir_base}.png, skipping')
                        else:
                            print(f'\t\t Found starfish in image {image_set+i}__{src_sub_dir_base}.png, saving to {image_path}')
                            if os.path.exists(image_path) != True:
                                cv2.imwrite(image_path, cropped_image)
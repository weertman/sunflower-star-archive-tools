import os
import glob
from multiprocessing import Pool
from PIL import Image
from heic2png import HEIC2PNG
from tqdm import tqdm

def find_files(directory, extensions):
    """Find files with given extensions in the directory, case insensitively."""
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(directory, f'*.{ext}')))
        files.extend(glob.glob(os.path.join(directory, f'*.{ext.upper()}')))
    return files

def rename_and_convert(file_data):
    file_path, target_dir = file_data
    new_file_path = file_path.replace(' ', '-')
    if new_file_path != file_path:
        os.rename(file_path, new_file_path)
        file_path = new_file_path
        print(f"Renamed to {new_file_path}")

    base_name = os.path.basename(os.path.splitext(file_path)[0])
    dst_png_file = os.path.join(target_dir, f'{base_name}.png')

    if os.path.exists(dst_png_file):
        print(f"File {dst_png_file} already exists")
        return

    # Ensure the correct output format is passed to the save method
    if file_path.lower().endswith('heic'):
        img = HEIC2PNG(file_path, quality=100)
        img.save(dst_png_file.replace('.png', '.PNG'))  # Explicitly use .PNG for HEIC2PNG
    else:
        img = Image.open(file_path)
        img.save(dst_png_file, "PNG")
    print(f"\t\tConverted {file_path} to {dst_png_file}")

def process_directory(root_data_dir, target_dir):
    print(f"Processing directory: {root_data_dir}")
    print()
    extensions = ['heic', 'jpeg', 'jpg']
    files = find_files(root_data_dir, extensions)
    print(f"Found {len(files)} files to convert in {root_data_dir}.")

    if files:
        file_data = [(f, target_dir) for f in files]
        with Pool(processes=8) as pool:
            pool.map(rename_and_convert, file_data)
    else:
        print("No files to convert.")

def main():
    root_data_dir = r'C:\Users\wlwee\Downloads\4-6-snug'
    if not os.path.exists(root_data_dir):
        print(f"Error: Directory {root_data_dir} does not exist.")
        return

    png_file_dir_name = '4_6_2024_releases'
    target_root_dir = os.path.join(root_data_dir, png_file_dir_name)

    if not os.path.exists(target_root_dir):
        os.makedirs(target_root_dir)
        print(f"Created directory {target_root_dir}")

    sub_dirs = [sub_dir for sub_dir in glob.glob(os.path.join(root_data_dir, '*')) if os.path.isdir(sub_dir) and os.path.basename(sub_dir) != png_file_dir_name]

    for sub_dir in tqdm(sub_dirs, desc="Processing Subdirectories"):
        target_sub_dir = os.path.join(target_root_dir, os.path.basename(sub_dir))
        if not os.path.exists(target_sub_dir):
            os.makedirs(target_sub_dir)
            print(f"Created subdirectory {target_sub_dir}")
        target_sub_dir = os.path.join(target_sub_dir, png_file_dir_name)
        if not os.path.exists(target_sub_dir):
            os.makedirs(target_sub_dir)
            print(f"\tCreated subdirectory {target_sub_dir}")

        process_directory(sub_dir, target_sub_dir)

if __name__ == "__main__":
    main()
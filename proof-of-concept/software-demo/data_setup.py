import os
import json
import shutil
from ultralytics.data.converter import convert_coco
import numpy as np

# directory where all PNG images are stored
png_dir = r'yolo_training\PNG'
# directory where the COCO JSON files are stored
coco_annotation_dir = r'yolo_training\COCO'
output_image_dir = r'dataset\images'
output_label_dir = r'dataset\labels'
converted_label_dir = r'coco_converted\labels'

# move PNGs to train, val, and test folders
def organize_images(split):
    # load the JSON file for the split
    json_file = os.path.join(os.getcwd(), coco_annotation_dir, f'{split}.json')
    with open(json_file, 'r') as f:
        coco_data = json.load(f)
    
    # extract image data
    images = coco_data['images']
    
    # move each image to the appropriate folder
    for image in images:
        image_file = image['file_name']
        source_path = os.path.join(os.getcwd(), png_dir, image_file)
        target_path = os.path.join(os.getcwd(), output_image_dir, split, image_file)
        
        if os.path.exists(source_path):
            shutil.copy(source_path, target_path)
        else:
            print(f"Warning: {source_path} does not exist")

    print(f'split data have been transferred to {os.path.join(os.getcwd(), output_image_dir, split)}')

def copy_converted_labels(source, target):
    # ensure the destination directory exists
    if not os.path.exists(target):
        os.makedirs(target)
    
    # copy all files from src_dir to dest_dir
    for filename in os.listdir(source):
        src_file = os.path.join(source, filename)
        dest_file = os.path.join(target, filename)
        
        # only copy if it's a file
        if os.path.exists(src_file):
            shutil.copy(src_file, dest_file)

# normalize converted labels such that the coordinates are within bounds
def read_files(directory):
    """Read all files in the specified directory."""
    files_data = {}
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filepath.endswith('.txt'):
            with open(filepath, 'r') as file:
                files_data[filepath] = file.readlines()
    return files_data

def normalize_coordinates(data):
    """Normalize coordinates and ensure they are within bounds."""
    normalized_lines = []
    #Oringinal code
    """for line in data:
        numbers = [float(num) for num in line.split()]
        normalized_numbers = []
        for num in numbers:
            normalized_num = max(0.0, min(1.0, num))
            normalized_numbers.append(normalized_num)

        normalized_lines.append(" ".join(map(str, normalized_numbers)) + "\n")
    return normalized_lines"""
    
    for line in data:
        numbers = np.array(list(map(float, line.split())))

        # Normalize the numbers
        normalized_numbers = np.clip(numbers, 0.0, 1.0)
        normalized_lines.append(" ".join(map(str, normalized_numbers)) + "\n")
    
    return normalized_lines

def write_files(files_data):
    """Write the normalized data back to the files."""
    for filepath, data in files_data.items():
        with open(filepath, 'w') as file:
            file.writelines(data)

def normalize_labels(directory):
    files_data = read_files(directory)
    for filepath, data in files_data.items():
        files_data[filepath] = normalize_coordinates(data)
    write_files(files_data)
    print(f"labels normalized in {directory}")

if __name__ == "__main__":
    splits = ['train', 'val', 'test']

    # organize train, val, and test images
    print("============== Transferring Images ==============")
    for split in splits:
        organize_images(split)

    # convert COCO labels to YOLO format (.txt)
    # TODO: there is a "save_dir" parameter for convert_coco method, but it doesn't seem to work with existing folder. Any workaround?
    print("\n============== Converting COCO Labels ==============")
    convert_coco("./yolo_training/COCO/", use_segments=False, use_keypoints=False, cls91to80=True)     # save to coco_converted by default
    print("labels converted from COCO to text files")

    print("\n============== Normalizing Labels ==============")
    for split in splits:
        # copy from coco_converted/labels to dataset/labels
        source = os.path.join(os.getcwd(), converted_label_dir, split)
        target = os.path.join(os.getcwd(), output_label_dir, split)
        copy_converted_labels(source, target)
        normalize_labels(target)
        print(f"normalized labels in {target}")
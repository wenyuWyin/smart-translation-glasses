### Directory Structure
| Item | Description |
|--------|--------|
| `text_extraction_test.py` | sample usage for tesseract text extraction and image blurness analysis |
| `data_setup.py` | set up folder structure for YOLO model training |
| `train_yolo_model.py` | train the YOLO model |
| `layout_analysis_test.py` | perform text extraction |
| `data.yaml` | basic information for YOLO model training |
| `yolo_training` | original training data downloaded from DocLayNet |

Another folder should be created to store YOLO-standard training data. The folder follows the structure below:
```
├── yolo_training
│   ├── COCO
│   │   ├── train.json
│   │   ├── test.json
│   │   ├── val.json
│   ├── PNG
├── dataset
│   ├── images
│   │   ├── test
│   │   ├── train
│   │   ├── val
│   ├── labels
│   │   ├── test
│   │   ├── train
│   │   ├── val
```

### How to Use
If a completed `capstone_yolov8_trained.pt` model is not currently in your root folder, please check ***How to train yolov8.pt***.\
Rename the png file as `target.png`, then use the trained model by running the `layout_analysis_test.py` script.

### How to train `yolov8.pt`
1. After ensuring the folder structure specified above, run `data_setup.py`.
2. Check if the images and labels are in appropriate folders, modify `data.yaml` to correct directory.
3. Run `train_yolo_model_test.py` to train the YOLO model with Nvdia GPU.

### Requirement
1. Download data set from [here](https://codait-cos-dax.s3.us.cloud-object-storage.appdomain.cloud/dax-doclaynet/1.0.0/DocLayNet_core.zip). Unzip the content into `yolo_training` folder.
2. Run `pip install -r requirements.txt` to install all the required dependencies.


Used technologies/data sources: YOLO from Ultralytics, PaddleOCR, Hugging Face, DocLayNet
Step 1 - Download the DocLayNet data set from Hugging Face for training, validating, and testing the image layout analysis machine learning model.


Note: The "PNG" folder is a giant folder that contains all the images for training, validation and testing.
Step 2 - Since YOLO model training is not fully compatible with training labels in COCO format, the directory structure above needs to be converted to a standard structure specified in YOLO documentation (https://docs.ultralytics.com/modes/train/). 
Step 2.0 - Create a new structure for the data set.

Step 2.1 - Split images for training, validation, and testing from the "PNG" folder. Categorize images in the appropriate folder. 
Step 2.2 - Convert labels in JSON format to YOLO-compatible .txt format using Ultralytics API (coco_convert)
Step 2.3 - Handle failed edge cases during coco_convert
https://github.com/ultralytics/yolov5/issues/10632 
Step 3 - Create a YAML file to specify data set details, including the categories of images and paths to training/validation/testing data.
Step 4 - Train the model
Step 5 - Predict

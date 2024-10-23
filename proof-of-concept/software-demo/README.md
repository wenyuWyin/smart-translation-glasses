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
After ensuring the folder structure specified above, run `data_setup.py`. Check if the images and labels are in appropriate folders. Run `train_yolo_model_test.py` to train the YOLO model. Use the trained model by running the `layout_analysis_test.py` script.

### Requirement
1. Download data set from [here](https://codait-cos-dax.s3.us.cloud-object-storage.appdomain.cloud/dax-doclaynet/1.0.0/DocLayNet_core.zip). Unzip the content into `yolo_training` folder.
2. Run `pip install -r requirements.txt` to install all the required dependencies.
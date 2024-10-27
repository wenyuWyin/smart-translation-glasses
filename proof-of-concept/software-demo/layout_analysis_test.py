# from paddleocr import PaddleOCR
# import cv2

# # Initialize PaddleOCR model
# ocr = PaddleOCR(use_angle_cls=True, lang='en')

# # Load the image
# image_path = 'sample2.png'
# image = cv2.imread(image_path)

# # Perform OCR
# result = ocr.ocr(image_path, cls=True)

# # Print OCR results (text and bounding boxes)
# for line in result:
#     for word_info in line:
#         print(f"Text: {word_info[1][0]}, Confidence: {word_info[1][1]}")
#         print(f"Bounding Box: {word_info[0]}")

# =================================================================
from ultralytics import YOLO
import cv2
from paddleocr import PaddleOCR

# use a pre-trained model
# model = YOLO("yolo11n.pt")

# use a customized model
model = YOLO("capstone_yolov8_trained.pt")

ocr = PaddleOCR(use_angle_cls=True, lang='en')

source = "target.png"
image = cv2.imread(source)

results = model(image) 

for result in results:
    result.show()
    boxes = result.boxes.xyxy
    
    # iterate all the bounding boxes
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box)
        sub_image = image[y1:y2, x1:x2]

        # !! uncomment to show the bounding box images
        # cv2.imshow(f'Sub-image {i}', sub_image)
        # cv2.waitKey(0)

        # concatenate strings in one image
        extracted_string = ""
        print(f'============= Sub-image {i} =============')
        text_extraction_result = ocr.ocr(sub_image, cls=True)
        print(f'number of lines: {len(text_extraction_result)}')
        for line in text_extraction_result:
            print(f'number of words in a line: {len(line)}')
            for word_info in line:
                extracted_string += word_info[1][0] + " "
            
        print(f'extracted string: {extracted_string}')

cv2.destroyAllWindows()
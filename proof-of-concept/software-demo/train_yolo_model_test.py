import torch

# print(torch.cuda.is_available())  # Should return True if CUDA is available
# print(torch.cuda.device_count())  # Number of GPUs available
# print(torch.cuda.get_device_name(0))  

from ultralytics import YOLO
import os

# cuda and cudnn required
def main():
    # use GPU
    torch.cuda.set_device(0)

    cwd = os.getcwd()

    data_yaml = os.path.join(cwd, 'data.yaml')
    model_weights = 'yolov8n.pt'

    model = YOLO(model_weights)
    model = model.to('cuda')

    # train the model
    results = model.train(data=data_yaml, epochs=5, imgsz=640, batch=16, device=0, workers=4, amp=True, cache=False)

    model.val()
    # save the model
    model.save('capstone_yolov8_trained.pt')

if __name__ == "__main__":
    main()
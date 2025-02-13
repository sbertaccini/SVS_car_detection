from ultralytics import YOLO
import torch

def train_model():
    # Load a pretrained YOLOv8 model
    model = YOLO("yolov8n.pt")  # Options: yolov8n.pt, yolov8s.pt, yolov8m.pt for different size

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # Train the model
    model.train(data="car_detection.yaml", epochs=50, batch=8, imgsz=300, device=device, workers=0)

    # Validate the model
    model.val()

if __name__ == '__main__':
    train_model()

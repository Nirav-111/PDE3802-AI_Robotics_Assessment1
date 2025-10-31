from ultralytics import YOLO
import torch


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device used: {device}")

model = YOLO("yolo11n-cls.pt")

model.train(
    data=r"C:\Users\ASUS\Desktop\AI in Robotics\DataSplit",
    epochs = 49,
    imgsz = 416,
    batch=32,
    dropout=0.1,
    patience=10,
    lr0=0.001,
    device=device,

)
import cv2
import tkinter as tk
from tkinter import Label, Button, Frame
import threading
from PIL import Image, ImageTk
from ultralytics import YOLO
import os

from arm_controller import ArmController

MODEL_PATH = os.path.join("models", "best.pt")


class FruitSorterUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fruit Sorting System")
        self.root.geometry("1000x780")
        self.root.configure(bg="#081c15")

        self.fruits_detected = 0

        header_frame = Frame(root, bg="#1b4332")
        header_frame.pack(pady=10, fill="x")

        Label(
            header_frame,
            text="~ Fruit Sorting System ~",
            font=("Arial", 26, "bold"),
            bg="#1b4332",
            fg="#b7e4c7"
        ).pack(pady=5)

        self.display_width = 750
        self.display_height = 420

        video_outer = Frame(root, bg="#1b4332")
        video_outer.pack(pady=15)

        self.video_label = Label(
            video_outer,
            bg="black",
            width=self.display_width,
            height=self.display_height,
            text="📷 Initializing Camera...",
            fg="#95d5b2",
            font=("Arial", 12)
        )
        self.video_label.pack(padx=10, pady=10)

        btn_frame = Frame(root, bg="#081c15")
        btn_frame.pack(pady=20)

        fruit_buttons = [
            ("APPLE", "apple"),
            ("BANANA", "banana"),
            ("ORANGE", "orange"),
            ("LEMON", "lemon"),
            ("POMEGRANATE", "pomegranate"),
            ("TOMATO", "tomato")
        ]

        self.arm = ArmController()

        for i, (label, fruit_key) in enumerate(fruit_buttons):
            btn = Button(
                btn_frame,
                text=label,
                font=("Arial", 14, "bold"),
                bg="#2d6a4f",
                fg="white",
                padx=30,
                pady=14,
                command=lambda f=fruit_key: self.send_to_arm_thread(f),
                relief="flat",
                cursor="hand2"
            )
            btn.grid(row=0, column=i, padx=10)

        self.status_label = Label(
            root,
            text="System Ready",
            bg="#1b4332",
            fg="#d8f3dc",
            font=("Arial", 13, "bold")
        )
        self.status_label.pack(pady=8, fill="x")

        self.cap = None
        self.running = False

        self.start_camera_feed()


    # Arm control
    
    def send_to_arm_thread(self, fruit_name):
        """Run arm movement in a separate thread to avoid freezing GUI."""
        threading.Thread(target=self.send_to_arm, args=(fruit_name,), daemon=True).start()

    def send_to_arm(self, fruit_name):
        self.status_label.config(text=f"Sorting: {fruit_name}...", fg="#ffd60a")
        try:
            self.arm.sort_fruit_by_type(fruit_name)
            self.status_label.config(text=f"✓ Sent to {fruit_name} basket", fg="#52b788")
        except Exception as e:
            self.status_label.config(text=f"Arm Error: {str(e)}", fg="#d62828")

    
    # Camera detection
    
    def start_detection_thread(self):
        if not self.running:
            threading.Thread(target=self.start_detection, daemon=True).start()

    def start_detection(self):
        if self.running:
            return

        self.status_label.config(text="Loading Model...", fg="#ffd60a")
        try:
            self.model = YOLO(MODEL_PATH)
        except Exception as e:
            self.status_label.config(text="Model Load Error", fg="#d62828")
            print("Model error:", e)
            return

        self.running = True
        self.status_label.config(text=" Detection Active", fg="#52b788")

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            results = self.model(frame, conf=0.5)
            r = results[0]

            annotated = frame.copy()
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = f"{self.model.names[cls_id]} {conf:.2f}"

                cv2.rectangle(annotated, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(annotated, label, (int(x1), int(y1) - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            annotated = self.resize_frame(annotated)
            self.update_video_label(annotated)

        self.status_label.config(text="Camera Active", fg="#52b788")

    def stop_detection(self):
        self.running = False

    
        # Camera feed
    def start_camera_feed(self):
        self.cap = cv2.VideoCapture(1)
        if not self.cap.isOpened():
            self.video_label.config(text="❌ Camera Not Found", fg="red")
            return

        # Initialize shared frame storage
        self.latest_frame = None
        self.last_annotated = None

        # Start showing the camera feed
        self.update_camera_feed()

        # ✅ Start YOLO detection automatically
        self.start_detection_thread()

    def update_camera_feed(self):
        """Always read camera and show raw or detection-annotated frame."""
        if self.cap is None:
            return

        ret, frame = self.cap.read()
        if ret:
            # Save raw frame for detection thread
            self.latest_frame = frame.copy()

            # If detection running AND annotated frame available → show YOLO output
            if self.running and self.last_annotated is not None:
                display = self.last_annotated
            else:
                display = frame

            display = self.resize_frame(display)
            self.update_video_label(display)

        # Continue feed at ~30 FPS
        self.root.after(33, self.update_camera_feed)


    def resize_frame(self, frame):
        h, w = frame.shape[:2]
        aspect_ratio = w / h

        if aspect_ratio > (self.display_width / self.display_height):
            new_w = self.display_width
            new_h = int(new_w / aspect_ratio)
        else:
            new_h = self.display_height
            new_w = int(new_h * aspect_ratio)

        return cv2.resize(frame, (new_w, new_h))


    def update_video_label(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        imgtk = ImageTk.PhotoImage(img)
        self.video_label.config(image=imgtk, text="")
        self.video_label.image = imgtk



if __name__ == "__main__":
    root = tk.Tk()
    app = FruitSorterUI(root)
    root.mainloop()

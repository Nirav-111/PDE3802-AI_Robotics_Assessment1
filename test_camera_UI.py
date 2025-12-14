import cv2 
import tkinter as tk 
from tkinter import Label, Button, Frame 
from PIL import Image, ImageTk 
from ultralytics import YOLO 
import os 
import threading 
 
MODEL_PATH = os.path.join("models", "best.pt") 
 
class FruitSorterUI: 
    def __init__(self, root): 
        self.root = root 
        self.root.title("Smart Fruit Sorting System for Farmers") 
        self.root.geometry("900x650") 
        self.root.configure(bg="#081c15")
 
        # Stats tracking
        self.fruits_detected = 0
        self.good_quality = 0
        self.rejected = 0
 
        header_frame = Frame(root, bg="#1b4332", relief="flat", bd=0) 
        header_frame.pack(pady=10, padx=15, fill="x") 
 
        self.title_label = Label( 
            header_frame, 
            text="🌾 Smart Fruit Sorting System 🍎", 
            font=("Arial", 22, "bold"), 
            bg="#1b4332", 
            fg="#b7e4c7",
            pady=10
        ) 
        self.title_label.pack() 
        
        self.subtitle_label = Label(
            header_frame,
            text="AI-Powered Agricultural Technology",
            font=("Arial", 10),
            bg="#1b4332",
            fg="#d8f3dc",
            pady=3
        )
        self.subtitle_label.pack()
 
        # STATS BAR
        stats_frame = Frame(root, bg="#2d6a4f", relief="flat", bd=0)
        stats_frame.pack(pady=8, padx=15, fill="x")
        
        stats_inner = Frame(stats_frame, bg="#2d6a4f")
        stats_inner.pack(pady=8)
        
        # Create 4 stat boxes
        self.stat_detected = self.create_stat_box(stats_inner, "0", "Detected", 0)
        self.stat_good = self.create_stat_box(stats_inner, "0", "Good", 1)
        self.stat_rejected = self.create_stat_box(stats_inner, "0", "Rejected", 2)
        self.stat_efficiency = self.create_stat_box(stats_inner, "0%", "Efficiency", 3)
 
        # VIDEO DISPLAY 
        video_outer_frame = Frame(root, bg="#1b4332", relief="flat", bd=0)
        video_outer_frame.pack(pady=8, padx=15)
        
        video_frame = Frame(video_outer_frame, bg="#1b4332") 
        video_frame.pack(padx=10, pady=10)
 
        self.video_label = Label( 
            video_frame, 
            bg="#000000", 
            text="📹 Camera Ready",
            fg="#95d5b2",
            font=("Arial", 11),
            width=85,
            height=15,
            justify="center"
        ) 
        self.video_label.pack() 

        # BUTTON SECTION 
        button_frame = Frame(root, bg="#081c15") 
        button_frame.pack(pady=12) 
 
        self.start_button = Button( 
            button_frame, 
            text="▶ START", 
            font=("Arial", 14, "bold"), 
            bg="#52b788", 
            fg="white", 
            padx=35, 
            pady=11, 
            command=self.start_detection_thread,
            cursor="hand2",
            relief="flat",
            bd=0,
            activebackground="#40916c",
            activeforeground="white"
        ) 
        self.start_button.grid(row=0, column=0, padx=12) 
 
        self.stop_button = Button( 
            button_frame, 
            text="⛔ STOP", 
            font=("Arial", 14, "bold"), 
            bg="#d62828", 
            fg="white", 
            padx=35, 
            pady=11, 
            command=self.stop_detection,
            cursor="hand2",
            relief="flat",
            bd=0,
            activebackground="#9d0208",
            activeforeground="white"
        ) 
        self.stop_button.grid(row=0, column=1, padx=12) 
 
        # STATUS SECTION
        status_frame = Frame(root, bg="#1b4332", relief="flat", bd=0)
        status_frame.pack(pady=8, padx=15, fill="x")
        
        status_inner = Frame(status_frame, bg="#1b4332")
        status_inner.pack(pady=8)
        
        self.status_indicator = Label(
            status_inner,
            text="●",
            font=("Arial", 14),
            bg="#1b4332",
            fg="#52b788"
        )
        self.status_indicator.pack(side="left", padx=4)
        
        self.status_label = Label(
            status_inner,
            text="System Ready",
            font=("Arial", 12, "bold"),
            bg="#1b4332",
            fg="#d8f3dc"
        )
        self.status_label.pack(side="left")
 
        # State 
        self.cap = None 
        self.running = False 
        self.display_width = 680
        self.display_height = 300
        
        # Auto-start camera feed on launch
        self.start_camera_feed()
        
    def create_stat_box(self, parent, value, label, column):
        """Helper to create stat display boxes"""
        container = Frame(parent, bg="#2d6a4f")
        container.grid(row=0, column=column, padx=14, pady=3)
        
        value_label = Label(
            container,
            text=value,
            font=("Arial", 20, "bold"),
            bg="#2d6a4f",
            fg="#d8f3dc"
        )
        value_label.pack()
        
        text_label = Label(
            container,
            text=label,
            font=("Arial", 10),
            bg="#2d6a4f",
            fg="#b7e4c7"
        )
        text_label.pack()
        
        return value_label
 
    # THREAD SAFE START 
    
    def start_detection_thread(self): 
        if not self.running:
            thread = threading.Thread(target=self.start_detection) 
            thread.daemon = True 
            thread.start() 
 

    # MAIN LIVE DETECTION LOOP 
    def start_detection(self): 
        if self.running:
            return  # Already running
            
        print("Starting AI detection...") 
        self.status_label.config(text="Loading AI model...", fg="#ffc300")
 
        print("Loading model:", MODEL_PATH) 
        
        try:
            model = YOLO(MODEL_PATH)
            self.status_label.config(text="✓ AI Detection Active", fg="#52b788")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.status_label.config(text="Model Error", fg="#d62828")
            return
 
        self.running = True 
 
        while self.running: 
            if self.cap is None or not self.cap.isOpened():
                break
                
            ret, frame = self.cap.read() 
            if not ret: 
                continue 
 
            # YOLO Detection 
            results = model(frame) 
            annotated_frame = results[0].plot() 
            
            # Update stats 
            detections = results[0].boxes
            if len(detections) > 0:
                self.fruits_detected = len(detections)
                # Update stat displays
                self.stat_detected.config(text=str(self.fruits_detected))
 
            # Resize frame to fit display area 
            h, w = annotated_frame.shape[:2]
            aspect = w / h
            
            if aspect > (self.display_width / self.display_height):
                new_w = self.display_width
                new_h = int(new_w / aspect)
            else:
                new_h = self.display_height
                new_w = int(new_h * aspect)
            
            resized_frame = cv2.resize(annotated_frame, (new_w, new_h))
 
            # Convert BGR to RGB for Tkinter 
            rgb = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB) 
            img = Image.fromarray(rgb) 
            imgtk = ImageTk.PhotoImage(img) 
 
            # Update the label with new frame
            self.video_label.config(image=imgtk, text="", width=new_w, height=new_h) 
            self.video_label.image = imgtk
            
            # Process Tkinter events to keep UI responsive
            self.root.update()
        
        # When detection stops, resume normal camera feed
        print("AI detection stopped.") 
        self.status_label.config(text="Camera Active", fg="#52b788")
 
    def stop_detection(self): 
        print("Stopping detection...") 
        self.running = False
        

    # CAMERA FEED 
    def start_camera_feed(self):
        """Start camera feed immediately when UI launches"""
        print("Initializing camera...")
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            self.status_label.config(text="Camera Error", fg="#d62828")
            self.video_label.config(text="❌ Camera Not Found", fg="#d62828")
            return
        
        self.status_label.config(text="Camera Active", fg="#52b788")
        self.update_camera_feed()
    
    def update_camera_feed(self):
        
        if self.cap is None or not self.cap.isOpened():
            return
            
        ret, frame = self.cap.read()
        
        if ret:
            # Resize frame
            h, w = frame.shape[:2]
            aspect = w / h
            
            if aspect > (self.display_width / self.display_height):
                new_w = self.display_width
                new_h = int(new_w / aspect)
            else:
                new_h = self.display_height
                new_w = int(new_h * aspect)
            
            resized_frame = cv2.resize(frame, (new_w, new_h))
            
            # Convert to RGB for Tkinter
            rgb = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            imgtk = ImageTk.PhotoImage(img)
            
            # Update label
            self.video_label.config(image=imgtk, text="", width=new_w, height=new_h)
            self.video_label.image = imgtk
        
        # Schedule next update 
        if self.cap is not None:
            self.root.after(33, self.update_camera_feed)
 
 
# Run UI 
if __name__ == "__main__":
    root = tk.Tk() 
    app = FruitSorterUI(root) 
    root.mainloop()
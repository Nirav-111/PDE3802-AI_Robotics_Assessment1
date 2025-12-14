"""Live fruit detection with arm control integration."""
from ultralytics import YOLO
import cv2
import os
import time
from arm_controller import ArmController
from utils import load_config

# Path to your trained YOLOv8 model
MODEL_PATH = os.path.join("models", "best.pt")
CONFIG_PATH = os.path.join("config", "color_mapping.yaml")

def try_camera(index):
    """Try to open a camera at a given index."""
    cap = cv2.VideoCapture(index, cv2.CAP_V4L2)  # Use V4L2 backend for Linux
    time.sleep(1)  # Give time for camera to initialize

    if cap.isOpened():
        ret, _ = cap.read()
        if ret:
            return True, cap

    return False, None

def detect_fruit_and_sort(frame, model, arm_controller, config):
    """
    Detect fruit in frame and sort using arm controller.
    Returns detected fruit name if found, None otherwise.
    """
    # Run YOLO inference
    results = model(frame, conf=0.5, verbose=False)
    
    detected_fruits = []
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            class_name = result.names[cls_id]
            
            detected_fruits.append({
                'name': class_name,
                'confidence': conf,
                'bbox': box.xyxy[0].cpu().numpy()
            })
    
    return detected_fruits

def draw_detections(frame, detections):
    """Draw detection boxes on frame."""
    for det in detections:
        x1, y1, x2, y2 = det['bbox'].astype(int)
        label = f"{det['name']} ({det['confidence']:.2f})"
        
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    return frame

def main_live_detection(use_arm=True, sorting_mode='fruit'):
    """
    Main function for live fruit detection with optional arm sorting.
    
    Args:
        use_arm: Whether to control the arm (True) or just show detection (False)
        sorting_mode: 'fruit' for fruit-type sorting, 'color' for color-based sorting
    """
    print("="*60)
    print(f"LIVE FRUIT DETECTION - {sorting_mode.upper()} SORTING")
    print("="*60)
    print("Controls:")
    print("  'q' - Quit")
    print("  's' - Sort the detected fruit")
    print("  'Space' - Process next detection")
    print("="*60)

    # Try opening cameras at different indices
    print("Trying to open cameras...")

    success, cap = None, None
    for idx in [0, 1, 2]:  # Try index 0, then 1, then 2
        print(f"Trying camera index {idx}...")
        success, cap = try_camera(idx)
        if success:
            break

    if not success:
        print("Error: Could not open any camera!")
        return

    print("Camera opened successfully!")

    # Load YOLO model
    print(f"Loading YOLO model from {MODEL_PATH}...")
    model = YOLO(MODEL_PATH)
    
    # Load config
    config = load_config(CONFIG_PATH)
    
    # Initialize arm controller if requested
    arm_controller = None
    if use_arm:
        try:
            arm_controller = ArmController(config)
            print("Arm controller initialized!")
        except Exception as e:
            print(f"Warning: Could not initialize arm controller: {e}")
            print("Continuing with detection only...")

    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    time.sleep(2)  # Give camera time to warm up

    print("Starting live detection...\n")

    last_detections = []
    paused = False

    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to grab frame")
            break

        # Detect fruits
        detections = detect_fruit_and_sort(frame, model, arm_controller, config)
        
        if not paused:
            last_detections = detections

        # Draw detections
        annotated = draw_detections(frame.copy(), last_detections)
        
        # Add info text
        info_text = f"Detections: {len(last_detections)} | Mode: {sorting_mode.upper()}"
        cv2.putText(annotated, info_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        if paused:
            cv2.putText(annotated, "PAUSED - Press SPACE to continue", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display
        cv2.imshow(f"Live Fruit Detection [{sorting_mode}]", annotated)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Quitting...")
            break
        elif key == ord('s') and len(last_detections) > 0:
            # Sort the first detected fruit
            fruit = last_detections[0]
            print(f"\nSorting detected fruit: {fruit['name']}")
            
            if arm_controller:
                if sorting_mode == 'fruit':
                    arm_controller.sort_fruit_by_type(fruit['name'])
                else:  # color mode
                    # For color mode, pass the detected color
                    arm_controller.sort_fruit_by_color(fruit['name'])
            else:
                print("Arm controller not available!")
                
        elif key == ord(' '):
            paused = not paused
            status = "PAUSED" if paused else "RUNNING"
            print(f"Detection {status}")

    cap.release()
    cv2.destroyAllWindows()
    print("Detection stopped.")

if __name__ == "__main__":
    # Run with arm control in fruit-type sorting mode
    main_live_detection(use_arm=True, sorting_mode='fruit')

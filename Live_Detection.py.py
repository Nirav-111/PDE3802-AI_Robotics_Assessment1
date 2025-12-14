import cv2
import time
from ultralytics import YOLO

# Import DOFBOT functions
from dofbot_arm_control import (
    FRUIT_TO_BASKET,
    grab_from_pick_and_place
)

VALID_CLASSES = list(FRUIT_TO_BASKET.keys())

# Load YOLO model

print("[YOLO] Loading best.pt...")
model = YOLO("best.pt")
print("[YOLO] Model loaded.")

# Camera setup

def try_camera(idx):
    cap = cv2.VideoCapture(idx)
    time.sleep(1)
    if cap.isOpened():
        ok, _ = cap.read()
        if ok:
            return cap
    return None

cap = None
for i in [0, 1, 2]:
    print(f"[CAMERA] Trying index {i}...")
    cap = try_camera(i)
    if cap:
        print(f"[CAMERA] Active at index {i}.")
        break

if not cap:
    raise RuntimeError("ERROR: NO CAMERA FOUND!")

cap.set(3, 640)
cap.set(4, 480)

# Detection function

def detect_fruit(frame):
    """Return (class_name, confidence) of best valid detection."""
    results = model(frame, imgsz=640, conf=0.5, verbose=False)

    best_class = None
    best_conf = 0.0

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            name = r.names[cls_id].lower()

            if name in VALID_CLASSES and conf > best_conf:
                best_class = name
                best_conf = conf

    return best_class, best_conf

# MAIN LOOP

print("[SYSTEM] Live detection running.")
print("Press 's' to SORT | 'q' to QUIT")

last_detected = None

while True:

    ok, frame = cap.read()
    if not ok:
        continue

    cls, conf = detect_fruit(frame)
    
    if cls:
        last_detected = cls
        cv2.putText(frame,
                    f"{cls} ({conf:.2f})",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (0, 255, 0),
                    2)

    cv2.imshow("Fruit Detection", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        print("[SYSTEM] Exiting...")
        break

    if key == ord('s'):
        if last_detected:
            print(f"[SYSTEM] Sorting {last_detected}...")
            pose = FRUIT_TO_BASKET[last_detected]
            grab_from_pick_and_place(pose, label=last_detected)
        else:
            print("[SYSTEM] No fruit detected yet.")


# Shutdown
cap.release()
cv2.destroyAllWindows()
print("[SYSTEM] Shutdown complete.")

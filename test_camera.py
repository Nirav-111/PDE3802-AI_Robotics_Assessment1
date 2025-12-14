"""Test camera"""
import cv2

# Try to open camera 0
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("[ERROR] Could not open camera at index 0.")
    print("Check connection, camera index, or permissions.")
    exit(1)

print("Press 'q' to quit")

while True:
    ret, frame = cap.read()

    if not ret:
        print("[ERROR] Failed to read frame from camera.")
        break

    cv2.imshow('Camera', frame)

    # Quit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Camera works!")

from ultralytics import YOLO

# Load your trained model
model = YOLO(r"C:\Users\assen_i0mhc8l\Downloads\ezyZip (2)\runs\classify\train4\weights\best.pt")

# The 7 valid classes you trained the model on
VALID_CLASSES = ["chair", "desk", "headphones", "laptop", "mouse", "mug", "printer"]

def predict_image(image_path):
    """
    Takes an image file path, runs YOLO classification,
    and returns the predicted class name and confidence score.
    Only returns valid predictions above a confidence threshold.
    """
    results = model.predict(source=image_path, save=False)
    probs = results[0].probs

    predicted_class = results[0].names[probs.top1]
    confidence = probs.top1conf.item() * 100

    # Set minimum confidence threshold
    THRESHOLD = 60  # adjust as needed (60% is a good starting point)

    if predicted_class not in VALID_CLASSES or confidence < THRESHOLD:
        return "Unknown Object", confidence
    else:
        return predicted_class, confidence


# Manual test
if __name__ == "__main__":
    test_image = r"C:\Users\ASUS\Desktop\AI in Robotics\DataSplit\test\mug\1.jpg"
    label, conf = predict_image(test_image)
    print(f"Prediction: {label} ({conf:.2f}%)")

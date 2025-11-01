# PDE3802-AI_Robotics_Assessment1
AI in Robotics – Autonomous Office Organizer System (Assessment 1, PDE3802)


Overview
This project was completed for the Middlesex University module *Artificial Intelligence in Robotics (PDE3802)*.  
It focuses on developing a vision-based classification system capable of recognising common office items using deep learning.  
The system applies the YOLO framework to identify objects such as chairs, mugs, and laptops, and demonstrates how AI and computer vision can be integrated into robotics to improve perception and autonomy.



Project Objectives
- Develop a reliable image classification model for office object recognition.  
- Prepare and structure a dataset for effective model training and testing.  
- Apply transfer learning using YOLO to enhance performance and reduce training time.  
- Implement simple user interfaces for local and web-based testing.  
- Evaluate accuracy, F1-score, and confusion matrix results to assess model performance.


Project Structure
| File                            | Description                                                        |
--------------------------------------------------------------------------------------------------------
| `dataset.py`                    | Splits raw image data into training, validation, and test folders. 
| `datasplit_organise.py`         | Prepares and arranges dataset folders for YOLO compatibility. 
| `tain.py`                       | Trains the YOLO classification model on the dataset. 
| `predict_yolo.py`               | Loads the trained model and predicts an object class from an image. 
| `frontend.py`                   | Tkinter desktop interface for image selection and prediction. 
| `application.py`                | Streamlit web interface for real-time image classification. 
| `yolo11n.pt` / `yolo11n-cls.pt` | Pre-trained YOLO weights used for model fine-tuning. 



Classes Used
The model was trained on seven office-related classes:

`chair, desk, headphones, laptop, mouse, mug, printer`



Installation and Setup

1. Clone the Repository
```bash
git clone https://github.com/Nirav-111/PDE3802-AI_Robotics_Assessment1.git
cd PDE3802-AI_Robotics_Assessment1
````

2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

3. Install Required Packages

```bash
pip install ultralytics torch pillow streamlit
```

4. Train the Model (Optional)

Update dataset paths in `tain.py` and run:

```bash
python tain.py
```

5. Run the Desktop App

```bash
python frontend.py
```

6. Run the Web App

```bash
streamlit run application.py
```



Model Summary

* Framework: YOLOv11-classify
* Image size: 416 × 416 pixels
* Epochs: 49
* Batch size: 32
* Learning rate: 0.001
* Evaluation metrics: Accuracy, Macro F1-score, Confusion Matrix

The model achieved reliable results across all seven categories and maintained stable performance during real-time testing on both desktop and Raspberry Pi 4 systems.



Interfaces

Desktop application: A lightweight Tkinter interface for local image testing.
Web application:  A Streamlit interface for live image upload and classification.



Results

* Dataset divided into 80% training, 10% validation, and 10% testing.
* Consistent prediction accuracy across all classes.
* Fast inference and efficient memory use.
* Clear output displaying predicted class and confidence level.



References

* Middlesex University (2025–26). *Artificial Intelligence in Robotics – PDE3802 Module Handbook.*
* Ultralytics Documentation: [https://docs.ultralytics.com](https://docs.ultralytics.com)
* PyTorch Documentation: [https://pytorch.org/docs](https://pytorch.org/docs)
* OpenCV Documentation: [https://docs.opencv.org](https://docs.opencv.org)



Author

Nirav Motee Soomarchun
Middlesex University Mauritius
Student ID: M00905630



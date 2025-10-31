import streamlit as st
from PIL import Image
from ultralytics import YOLO

model = r"C:\Users\ASUS\Desktop\AI in Robotics\runs\classify\train4\weights\best.pt"
modell = YOLO(model)

st.set_page_config(page_title = "AI in Robotics")
st.title("AI in Robotics")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)


    results = modell.predict(image)

    probs = results[0].probs
    names = results[0].names
    top_class = names[probs.top1]
    confidence = probs.top1conf.item()

    st.success(f"Top class : {top_class} (confidence: {confidence*100:.2f}%)")

    st.subheader("Class Probabilities")
    for i, p in enumerate(probs.data.tolist()):
        st.write(f"{names[i]}: {p*100:.2f}%")
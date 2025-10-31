import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from predict_yolo import predict_image  

# --- Functions ---
def open_file():
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    if file_path:
        try:
            # Predict using YOLO
            label, confidence = predict_image(file_path)
            result_label.config(text=f"{label} ({confidence:.2f}%)")

            # Visual feedback for result
            if label == "Unknown Object":
                result_label.config(
                    text=f"⚠️ {label} ({confidence:.1f}%)",
                    fg="#e53935"  # red
                )
                status_label.config(
                    text="⚠️ Not one of the 7 allowed items",
                    fg="#e53935"
                )
            else:
                color = "#2e7d32" if confidence >= 85 else "#fb8c00"
                emoji = "✅" if confidence >= 85 else "🟡"
                result_label.config(
                    text=f"{emoji} {label.capitalize()} ({confidence:.1f}%)",
                    fg=color
                )
                status_label.config(text="✅ Prediction Complete", fg="#2e7d32")
                
            # Show image
            img = Image.open(file_path)
            img.thumbnail((180, 180))  # smaller preview
            img_tk = ImageTk.PhotoImage(img)
            image_label.config(image=img_tk)
            image_label.image = img_tk

            status_label.config(text="Prediction completed ✅", fg="#2e7d32")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")
            status_label.config(text="Error occurred ❌", fg="#d32f2f")

# Button hover effect
def on_enter(e):
    e.widget['background'] = '#1565c0'
    e.widget['foreground'] = 'white'

def on_leave(e):
    e.widget['background'] = '#2196f3'
    e.widget['foreground'] = 'white'

# --- Root Window ---
root = tk.Tk()
root.title("AI Office Item Classifier")
root.geometry("400x400")  # smaller size
root.configure(bg="#f0f2f5")
root.resizable(False, False)

# --- Title ---
title_label = tk.Label(root, text="Smart Office Item Classifier", 
                       font=("Helvetica", 16, "bold"), bg="#f0f2f5", fg="#333333")
title_label.pack(pady=10)

# --- Image Preview ---
image_label = tk.Label(root, bg="#f0f2f5", bd=2, relief="groove")
image_label.pack(pady=10)

# --- Select Button ---
select_button = tk.Button(root, text="Select Image", font=("Helvetica", 12, "bold"),
                          bg="#2196f3", fg="white", padx=15, pady=8, command=open_file, relief="raised", bd=2)
select_button.pack(pady=10)
select_button.bind("<Enter>", on_enter)
select_button.bind("<Leave>", on_leave)

# --- Prediction Result ---
result_label = tk.Label(root, text="", font=("Helvetica", 12, "bold"), bg="#f0f2f5", fg="#333333")
result_label.pack(pady=8)

# --- Status Bar ---
status_label = tk.Label(root, text="Ready", font=("Helvetica", 10), bg="#f0f2f5", fg="#333333")
status_label.pack(side="bottom", pady=5)

root.mainloop()

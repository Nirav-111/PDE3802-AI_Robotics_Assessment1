import os
import shutil

maindataset_path=r"C:\Users\ASUS\Desktop\AI in Robotics\dataset"

image_extension=(".jpg",".jpeg",".png")

splits = ["train","valid","test"]

for split in splits:
    split_path=os.path.join(maindataset_path,split)
    if not os.path.exists(split_path):
        print(f"{split_path} does not exist")
        continue
    print(f"split folder: {split}")


    file = [ f for f in os.listdir(split_path) if f.lower().endswith(image_extension)]
    if not file:
        print(f"{split_path} does not contain any image")
        continue


    for f in file:
        file_path=os.path.join(split_path,f)
        class_name = f.split("_")[0] if"_" in f else "unknown"
        class_dir=os.path.join(split_path,class_name)

        os.mkdir(class_dir)
        shutil.move(file_path,os.path.join(class_dir,f))

        print(f" moved {len(file)} images in {split_path}")

print("\nDataset is now ready")
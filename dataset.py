import os
import shutil
import random

Dataset = r'C:\Users\ASUS\Desktop\AI in Robotics\dataset'
output_folder = r'C:\Users\ASUS\Desktop\AI in Robotics\DataSplit'




split_ratio = {
    'train': 0.8,
    'valid': 0.1,
    'test': 0.1
}

copy_files= True
random.seed(45)

def image_file(filename):
    return filename.lower().endswith(('.jpg', '.jpeg', '.png'))

categorize = [
    folder for folder in os.listdir(Dataset)
    if os.path.isdir(os.path.join(Dataset, folder)) and not folder.startswith('.')
]

print("categorize found:")



for split in split_ratio.keys():
    for category in categorize:
        os.makedirs(os.path.join(output_folder,split, category),exist_ok=True)


overall = 0
total_categories= {}
split_information = {}

for category in categorize:
    category_path = os.path.join(Dataset,category)
    photos =[]

    for root, dirs, files in os.walk(category_path):
        for f in files:
            if image_file(f):
                photos.append(os.path.join(root,f))

    total = len(photos)
    overall += total
    total_categories[category] = total


    if total == 0:
        print("No images in {}".format(category))
        continue

    random.shuffle(photos)



    train_count = int(total * split_ratio['train'])
    val_count= train_count + int(total * split_ratio['valid'])

    splits = {
        'train': photos[:train_count],
         'valid': photos[train_count:val_count],
          'test': photos[val_count:]
    }

    split_information[category] = {k: len(v) for k, v in splits.items()}

    for split_name, file_list in splits.items():
        dst_folder = os.path.join(output_folder, split_name, category)
        os.makedirs(dst_folder, exist_ok=True)
        for src_path in file_list:
            filename=os.path.basename(src_path)
            dst_path = os.path.join(dst_folder, filename)
            if copy_files:
               shutil.copy(src_path, dst_path)

    print(f"\n{category.upper()} - Total images: {total}")
    print("-" * 46)
    for split_name, count in split_information[category].items():
        print(f"{split_name.capitalize():<9}  {count:>6} images | {split_ratio[split_name] * 100:>5.2f}%")



print("\n" + "=" * 50)
print(f"{'Category':<11} {'train':>6} {'valid':>6} {'test':>6}")
print("-" * 50)

for category, counts in split_information.items():
    total_cat = total_categories[category]
    print(f"\n {category.capitalize():<11} {counts['train']:6} {counts['valid']:>6} {counts['test']:>6} {total_cat:>6}")
    print("=" * 50)

print(f"\n overall images : {overall}")
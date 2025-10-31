import os
import hashlib
import shutil


dataset = r'C:\Users\ASUS\Desktop\AI in Robotics\dataset'

duplicates = os.path.join(dataset, 'duplicates')

location_changed = True;

def hash_image(file_path):
    hasher = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error hashing {file_path}: {e}")
        return None

def removal_duplicates(base_folder):
    hashes = {}
    duplicatess = []

    for root, _, files in os.walk(base_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(root, file)
                hash_value = hash_image(file_path)

                if not hash_value:
                    continue

                if hash_value in hashes:
                    duplicatess.append(file_path)
                else:
                    hashes[hash_value] = file_path

    if not duplicatess:
        print("\n no duplicates")
        return

    os.makedirs(duplicates, exist_ok=True)

    print(f"\n {len(duplicates)} duplicates found")
    for dup in duplicatess:
          try:
              if location_changed:
                  shutil.move(dup, os.path.join(duplicates, os.path.basename(dup)))
              else:
                  os.remove(dup)
          except Exception as e:
              print(f"Error removing {dup}: {e}")

    print(f" Duplicates { 'location changed'if location_changed else 'deleted'}successfully.")
    print(f" Duplicates stored in: {duplicates}" if location_changed else "")

if __name__ == '__main__':
    removal_duplicates(dataset)





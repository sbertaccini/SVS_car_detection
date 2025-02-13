import os
import shutil
import random

# Define paths
dataset_path = "../dataset"
images_path = os.path.join(dataset_path, "images")
labels_path = os.path.join(dataset_path, "labels")

# Create train/val directories
for subdir in ["train", "val"]:
    os.makedirs(os.path.join(images_path, subdir), exist_ok=True)
    os.makedirs(os.path.join(labels_path, subdir), exist_ok=True)

# List all image files
image_files = [f for f in os.listdir(images_path) if f.endswith((".jpg", ".png", ".jpeg"))]

# Shuffle and split (e.g., 80% train, 20% val)
random.shuffle(image_files)
split_idx = int(len(image_files) * 0.8)
train_files = image_files[:split_idx]
val_files = image_files[split_idx:]

# Function to move files
def move_files(files, split):
    for file in files:
        image_src = os.path.join(images_path, file)
        label_src = os.path.join(labels_path, file.replace(file.split(".")[-1], "txt"))  # Convert extension to .txt
        
        image_dest = os.path.join(images_path, split, file)
        label_dest = os.path.join(labels_path, split, file.replace(file.split(".")[-1], "txt"))

        if os.path.exists(label_src):  # Ensure label file exists
            shutil.move(image_src, image_dest)
            shutil.move(label_src, label_dest)

# Move train and val files
move_files(train_files, "train")
move_files(val_files, "val")

print("Dataset split completed!")

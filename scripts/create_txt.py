import os

def create_txt_files(folder_path):
    # Ensure the folder exists
    if not os.path.isdir(folder_path):
        print("Folder not found!")
        return
    
    # Create subdirectory if it doesn't exist
    txt_folder = os.path.join(folder_path, "obj_train_data")
    os.makedirs(txt_folder, exist_ok=True)
    
    # Loop through each file in the folder
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(".png"):  # Check if it's a PNG image
            txt_file_path = os.path.join(txt_folder, os.path.splitext(file_name)[0] + ".txt")
            open(txt_file_path, 'w').close()  # Create an empty .txt file
            # print(f"Created: {txt_file_path}")

# Example usage
folder_path = "C:/Users/seren/UNIBO/MAGISTRALE/SVS/dataset_v2_distinct_lables/no_car"  # Replace with your actual folder path
create_txt_files(folder_path)

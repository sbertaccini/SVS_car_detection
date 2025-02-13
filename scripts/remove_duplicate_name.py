import os

def rename_duplicate_files(folder, start_number):
    counter = start_number

    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            # Check if the filename has a duplicate pattern (e.g., "name (2).png")
            name, ext = os.path.splitext(filename)
            if "(" in name and ")" in name:
                # Rename the file with an incremental number
                new_name = f"{counter}.png"
                os.rename(os.path.join(folder, filename), os.path.join(folder, new_name))
                counter += 1
    
    return counter

# Define folder paths
car_folder = "car"
no_car_folder = "no_car"

# Start renaming files in both folders
start_number = 50000
new_start = rename_duplicate_files(car_folder, start_number)
rename_duplicate_files(no_car_folder, new_start+1)
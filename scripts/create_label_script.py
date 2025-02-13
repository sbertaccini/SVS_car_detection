import os
import csv

def create_csv_from_folders(car_folder, no_car_folder, output_csv):
    data = []

    # Process "car" folder
    for filename in os.listdir(car_folder):
        if os.path.isfile(os.path.join(car_folder, filename)):
            data.append([filename, 1])

    # Process "no car" folder
    for filename in os.listdir(no_car_folder):
        if os.path.isfile(os.path.join(no_car_folder, filename)):
            data.append([filename, 0])

    # Write to CSV
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["file_name", "label"])
        writer.writerows(data)

# Define folder paths
car_folder = "car"
no_car_folder = "no_car"
output_csv = "dataset.csv"

# Create the CSV file
create_csv_from_folders(car_folder, no_car_folder, output_csv)
print(f"CSV file created at {output_csv}")
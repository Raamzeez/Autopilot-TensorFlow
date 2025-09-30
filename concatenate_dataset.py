import os
import shutil
import glob

def get_highest_image_number(folder_path):
    # Get all jpg files in the folder
    jpg_files = glob.glob(os.path.join(folder_path, '*.jpg'))
    if not jpg_files:
        return -1
    
    # Extract numbers from filenames and find highest
    numbers = [int(os.path.basename(f).split('.')[0]) for f in jpg_files]
    return max(numbers)

def merge_datasets(first_dataset_path, second_dataset_path, output_path):
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    # Get highest number from first dataset
    highest_num = get_highest_image_number(first_dataset_path)
    print(f"Highest number in first dataset: {highest_num}")
    
    # First, copy all files from first dataset to output
    for jpg_file in glob.glob(os.path.join(first_dataset_path, '*.jpg')):
        shutil.copy2(jpg_file, output_path)
    
    # Get and sort files from second dataset numerically
    second_dataset_files = glob.glob(os.path.join(second_dataset_path, '*.jpg'))
    second_dataset_files.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))

    # Copy data.txt from first dataset to output path
    shutil.copy2(os.path.join(first_dataset_path, 'data.txt'), output_path)
    
    with open(os.path.join(output_path, 'data.txt'), 'a') as f:
        num = highest_num + 1

        with open(os.path.join(second_dataset_path, 'data.txt'), 'r') as second_file:
            for jpg_file in second_dataset_files:
                line = second_file.readline()
                parts = line.strip().split(' ', 1)
                if len(parts) == 2:
                    f.write(f"{num}.jpg {parts[1]}\n") 
                destination = os.path.join(output_path, f"{num}.jpg")
                shutil.copy2(jpg_file, destination)

                num += 1


def main():
    # Define your paths here
    first_dataset_path = "driving_dataset"
    second_dataset_path = "driving_dataset_2"
    output_path = "joined_dataset"
    
    merge_datasets(first_dataset_path, second_dataset_path, output_path)
    print("Dataset merge completed successfully!")

if __name__ == "__main__":
    main()

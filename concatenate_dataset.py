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
    
    # Create mapping of old to new numbers for data.txt update
    number_mapping = {}
    next_num = highest_num + 1
    
    for jpg_file in second_dataset_files:
        old_num = int(os.path.basename(jpg_file).split('.')[0])
        new_filename = f"{next_num}.jpg"
        number_mapping[old_num] = next_num
        shutil.copy2(jpg_file, os.path.join(output_path, new_filename))
        next_num += 1
    
    print(f"Number mapping created: {len(number_mapping)} entries")
    print(f"Sample mapping: {dict(list(number_mapping.items())[:5])}")
    
    # Merge data.txt files
    output_data_path = os.path.join(output_path, 'data.txt')
    
    # First, copy first dataset's data.txt content
    with open(os.path.join(first_dataset_path, 'data.txt'), 'r') as first_file:
        first_dataset_data = first_file.read()
        
    with open(output_data_path, 'w') as f:
        f.write(first_dataset_data)
        # Ensure there's a newline at the end
        if not first_dataset_data.endswith('\n'):
            f.write('\n')
    
    # Read second dataset's data.txt and append with updated numbers
    with open(os.path.join(second_dataset_path, 'data.txt'), 'r') as f:
        second_dataset_lines = f.readlines()
    
    # Sort the lines from second dataset by their image numbers
    second_dataset_lines.sort(key=lambda x: int(x.split('.')[0]) if x.strip() else 0)
    
    with open(output_data_path, 'a') as f:
        for line in second_dataset_lines:
            line = line.strip()
            if not line:  # Skip empty lines
                continue
                
            parts = line.split(' ', 1)
            if len(parts) != 2:
                continue
                
            old_num = int(parts[0].split('.')[0])
            if old_num in number_mapping:
                new_line = f"{number_mapping[old_num]}.jpg {parts[1]}\n"
                f.write(new_line)
            else:
                print(f"Warning: Image {old_num}.jpg from second dataset not found, skipping...")

def main():
    # Define your paths here
    first_dataset_path = "driving_dataset_2"
    second_dataset_path = "driving_dataset_3"
    output_path = "joined_dataset"
    
    merge_datasets(first_dataset_path, second_dataset_path, output_path)
    print("Dataset merge completed successfully!")

if __name__ == "__main__":
    main()

import os
import glob

def trim_dataset(source_dir, starting_number, ending_number, confirm=True):
    """
    Trim a dataset by removing files outside a specified number range.
    
    Args:
        source_dir (str): Path to the directory containing the dataset
        starting_number (int): Keep files from this number onwards
        ending_number (int): Keep files up to this number
        confirm (bool, optional): Whether to ask for confirmation before deleting. Defaults to True.
    
    Returns:
        tuple: (files_kept, files_removed) counts
    """
    print(f"Trimming dataset: keeping files {starting_number}.jpg to {ending_number}.jpg")
    print(f"Source directory: {source_dir}")

    # Get all jpg files from source directory
    jpg_files = glob.glob(os.path.join(source_dir, "*.jpg"))
    print(f"Found {len(jpg_files)} total .jpg files")

    # Count files to be removed
    files_to_remove = 0
    files_to_keep = 0

    for image_path in jpg_files:
        # Extract the number from filename (e.g., "123.jpg" -> 123)
        filename = os.path.basename(image_path)
        file_number = int(filename.split('.')[0])
        
        # Check if file should be kept
        if starting_number <= file_number <= ending_number:
            files_to_keep += 1
        else:
            files_to_remove += 1

    print(f"Files to keep: {files_to_keep}")
    print(f"Files to remove: {files_to_remove}")

    # Confirm before proceeding
    if confirm:
        user_confirm = input("Proceed with trimming? (y/n): ")
        if user_confirm.lower() != 'y':
            print("Trimming cancelled.")
            return (0, 0)

    # Remove files outside the range
    removed_count = 0
    for image_path in jpg_files:
        filename = os.path.basename(image_path)
        file_number = int(filename.split('.')[0])
        
        # Remove file if outside range
        if not (starting_number <= file_number <= ending_number):
            try:
                os.remove(image_path)
                removed_count += 1
                if removed_count % 100 == 0:
                    print(f"Removed {removed_count} files...")
            except Exception as e:
                print(f"Error removing {filename}: {e}")

    # Process data.txt to remove corresponding lines
    data_file_path = os.path.join(source_dir, 'data.txt')
    
    # Read all lines first
    with open(data_file_path, 'r') as data_file:
        lines = data_file.readlines()
    
    # Filter lines to keep
    lines_to_keep = []
    for line in lines:
        if line.strip():  # Skip empty lines
            filename = line.split()[0]
            file_number = int(filename.split('.')[0])
            if starting_number <= file_number <= ending_number:
                lines_to_keep.append(line)
    
    # Write back the filtered lines
    with open(data_file_path, 'w') as data_file:
        data_file.writelines(lines_to_keep)

    print(f"Trimming complete! Removed {removed_count} files.")
    print(f"Kept files from {starting_number}.jpg to {ending_number}.jpg")
    
    return (files_to_keep, removed_count)

if __name__ == "__main__":
    # Example usage with default values
    source_dir = "driving_dataset_2"
    starting_number = 2
    ending_number = 6
    trim_dataset(source_dir, starting_number, ending_number)

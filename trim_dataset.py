import os
import glob

# Configuration
source_dir = "driving_dataset_4_cropped"
starting_number = 19  # Keep files from this number onwards
ending_number = 10620   # Keep files up to this number

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
confirm = input("Proceed with trimming? (y/n): ")
if confirm.lower() != 'y':
    print("Trimming cancelled.")
    exit()

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

print(f"Trimming complete! Removed {removed_count} files.")
print(f"Kept files from {starting_number}.jpg to {ending_number}.jpg")

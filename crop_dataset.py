import cv2
import os
import glob

# Source and destination directories
source_dir = "driving_dataset_2"
dest_dir = "driving_dataset_2_cropped"

# Create destination directory if it doesn't exist
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

# Get all jpg files from source directory
jpg_files = glob.glob(os.path.join(source_dir, "*.jpg"))
print(f"Found {len(jpg_files)} images to process...")

# Sort files numerically (not alphabetically)
jpg_files.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))
print(f"First 10 files: {[os.path.basename(f) for f in jpg_files[:10]]}")
print(f"Last 10 files: {[os.path.basename(f) for f in jpg_files[-10:]]}")

# Set max limit for processing (set to None for no limit)
MAX_IMAGES = 100  # Change this number or set to None for all images
if MAX_IMAGES:
    jpg_files = jpg_files[:MAX_IMAGES]
    print(f"Processing first {len(jpg_files)} images (limited by MAX_IMAGES)")

# Process each image
for i, image_path in enumerate(jpg_files):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not read image: {image_path}")
        continue
    
    # Get original dimensions
    height, width = img.shape[:2]
    
    # Crop using the same logic as run_dataset.py:
    # Remove bottom 1350 pixels (like in training: full_image[-1350:])
    # Remove right 1500 pixels (additional cropping for UI elements)
    existing_bottom_removed = -150 # The number of pixels that train.py is removing from the bottom
    window_cropped_img = img[:-1080, :-1920] # This is the crop we do to capture the window of the game
    cropped_img = window_cropped_img[:-existing_bottom_removed + existing_bottom_removed + -150, :]
    # ^ We remove an additional -150 pixels to get rid of the dashboard
    
    # Get the filename
    filename = os.path.basename(image_path)
    
    # Save the cropped image
    output_path = os.path.join(dest_dir, filename)
    cv2.imwrite(output_path, cropped_img)
    
    # Print progress
    if (i + 1) % 100 == 0:
        print(f"Processed {i + 1}/{len(jpg_files)} images...")

print(f"Done! Cropped images saved to {dest_dir}")
print(f"Original size: {width}x{height}")
print(f"Cropped size: {width-300}x{height-300}")

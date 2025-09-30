import os
from crop_dataset import crop_dataset
from trim_dataset import trim_dataset
from concatenate_dataset import merge_datasets

print("╔════════════════════════════════════════════════════════════════╗")
print("║                     Processing Dataset                         ║")
print("║--------------------------------------------------------------- ║")
print("║ Step 1: Cropping                                               ║")
print("║ Step 2: Trimming                                               ║")
print("║ Step 3: Concatenating                                          ║")
print("╚════════════════════════════════════════════════════════════════╝")

# Get user inputs
og_dataset_path = input("Enter the path to the original dataset: ")
existing_dataset_path = input("Enter the path to the existing large dataset to merge with: ")
new_dataset_path = input("Enter the path to the new large dataset after processing: ")
starting_number = int(input("Enter the starting image number for dataset: "))  # Convert to int
ending_number = int(input("Enter the ending image number for dataset: "))      # Convert to int

print(f"╔════════════════════════════════════════════════════════════════╗")
print(f"║                     Processing Dataset                         ║")
print(f"║----------------------------------------------------------------║")
print(f"║ Step 1: Cropping                                               ║")
print(f"║        Input:  {og_dataset_path:<21}                           ║")
print(f"║        Output: {og_dataset_path + '_cropped':<34}              ║")
print("╚════════════════════════════════════════════════════════════════╝")
print(f"║ Step 2: Trimming                                               ║")
print(f"║        Input:  {og_dataset_path + '_cropped':<34}              ║")
print(f"║        Output: {og_dataset_path:<34}              ║")
print(f"║        Range:  {starting_number} to {ending_number:<35}        ║")
print("╚════════════════════════════════════════════════════════════════╝")
print(f"║ Step 3: Concatenating                                          ║")
print(f"║        Dataset 1: {existing_dataset_path:<27}                  ║")
print(f"║        Dataset 2: {og_dataset_path:<35}          ║")
print(f"║        Output:    {new_dataset_path:<22}                       ║")
print("╚════════════════════════════════════════════════════════════════╝")

# Get confirmation
confirm = input("\nDoes the above information look correct? Press 'y' to proceed: ")

if confirm.lower() == 'y':
    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║                     Processing Started                         ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    
    crop_dataset(og_dataset_path, og_dataset_path + "_cropped")
    trim_dataset(og_dataset_path + "_cropped", starting_number, ending_number)
    os.rename(og_dataset_path, og_dataset_path + "_og")
    os.rename(og_dataset_path + "_cropped", og_dataset_path)
    merge_datasets(existing_dataset_path, og_dataset_path, new_dataset_path)
    
    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║                     Processing Complete                        ║")
    print("╚════════════════════════════════════════════════════════════════╝")
else:
    print("\nProcessing cancelled.")
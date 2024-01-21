import os
import shutil

def move_file_up(source_path):
    # Get the parent directory of the current file
    parent_directory = os.path.dirname(os.path.abspath(source_path))

    # Move the file to the parent directory
    destination_path = os.path.join(parent_directory, os.path.basename(source_path))
    print(parent_directory)
    print(destination_path)
    shutil.move(source_path, destination_path)

# Example usage
source_file = os.path.join(os.getcwd(), ".tmp", "c001", "0.jpg")
print(source_file)


move_file_up(source_file)
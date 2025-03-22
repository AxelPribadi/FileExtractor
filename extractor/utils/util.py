import os
import shutil

def move_files(file: str, src_path, dest_path):
    source_path = os.path.join(src_path, file)
    destination_path = os.path.join(dest_path, file)
    
    # Make sure the destination directory exists
    os.makedirs(dest_path, exist_ok=True)
    
    # Move the file
    shutil.move(source_path, destination_path)
    print(f"Moved {file} to processed folder")


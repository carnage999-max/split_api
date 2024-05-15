import time
import shutil
import os


def main():
    deleted_folders_count = 0
    deleted_files_count = 0
    path = ""

    seconds = time.time() - 60

    if os.path.exists(path):
        for root_folder, folders, files in os.walk(path):
            if seconds >= get_file_or_folder_age(folder_path):
                remove_folder(root_folder)
                deleted_folders_count += 1
                break 
            else:
                for folder in folders:
                    folder_path = os.path.join(root_folder, folder)
                    if seconds >= get_file_or_folder_age(folder_path):
                        remove_folder(folder_path)
                        deleted_folders_count += 1
                for file in files:
                    file_path = os.path.join(root_folder, file)
                    if seconds >= get_file_or_folder_age(folder_path):
                        remove_file(file_path)
                        deleted_files_count += 1
                        

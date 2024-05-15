import json
import os
import random
from pathlib import Path
import shutil


BASE_DIR = Path(__file__).resolve().parent.parent
filename = ''
num_lines = 0
file_size = 0
total_lines = 0
newpath = ''


def main():
    global newpath
    newpath = f'{BASE_DIR}/files/json/compress'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    # if the directory already exists, create a new folder with random numbers in the name
    else:
        newpath = f'{BASE_DIR}/files/json/compress{random.randint(1, 1000000)}'
        os.makedirs(newpath)
    with open(os.path.join(BASE_DIR, 'uploaded_files', filename), 'r') as f:
        data = json.load(f)
        total_lines = len(data)
        num_chunks = total_lines // num_lines + 1

        for i in range(num_chunks):
            start_idx = i * num_lines
            end_idx = start_idx + num_lines
            chunk_data = data[start_idx:end_idx]

            with open(os.path.join(newpath, f'chunk_{i}.json'), 'w') as chunk_file:
                json.dump(chunk_data, chunk_file)

        def get_all_file_paths(directory):
            file_paths = []

            for root, directories, files in os.walk(directory):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    file_paths.append(file_path)
            return file_paths

        def compress(source, destination):
            base = os.path.basename(newpath)
            name = base.split('.')[0]
            archive_from = os.path.dirname(source)
            archive_to = os.path.basename(source.strip(os.sep))
            print(source, destination, archive_from, archive_to)
            shutil.make_archive(name, 'zip', archive_from, archive_to)
            shutil.move('%s.%s' % (name, 'zip'), destination)

        compress(newpath, f'{newpath}/chunkedfiles.zip')

        for file in get_all_file_paths(newpath):
            if file != os.path.join(newpath, 'chunkedfiles.zip'):
                os.remove(file)


def remove_uploaded_file():
    os.remove(os.path.join(BASE_DIR, 'uploaded_files', filename))
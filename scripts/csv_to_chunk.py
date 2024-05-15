import os
import random
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent
filename = ''
number_of_lines = 0
newpath = ''
file_size = 0


def main():
    # create a new directory to store ~split files
    global newpath
    newpath = f'{BASE_DIR}/files/csv/compress'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    # if the directory already exists, create a new folder with random numbers in the name
    else:
        newpath = f'{BASE_DIR}/files/csv/compress{random.randint(1, 1000000)}'
        os.makedirs(newpath)
    # create the chunk files and write to it

    def write_chunk(part, lines):
        with open(os.path.join(newpath, f"data_part_{part}.csv"), 'w') as f_out:
            # write the header
            f_out.write(header)
            # write the remainder of the lines
            f_out.writelines(lines)

    # open the file to be split in read mode
    with open(os.path.join(BASE_DIR, 'uploaded_files', filename), 'r') as f:
        count = 0
        header = f.readline()
        lines = []
        for line in f:
            count += 1
            lines.append(line)
            if count % number_of_lines == 0:
                write_chunk(count // number_of_lines, lines)
                lines = []
        # write remainder
        if len(lines) > 0:
            write_chunk((count // number_of_lines) + 1, lines)

    # create a function to zip the split files
    # get the file paths of files to be zipped
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

    def remove_files():
        for file in get_all_file_paths(newpath):
            if file != os.path.join(newpath, 'chunkedfiles.zip'):
                os.remove(file)

    remove_files()


def remove_uploaded_file():
    os.remove(os.path.join(BASE_DIR, 'uploaded_files', filename))
from tqdm import tqdm
from PIL  import Image

import os


def copy_file(src:str, dest:str):
    with open(src, 'rb') as f:
        data = f.read()
    with open(dest, 'wb') as f:
        f.write(data)




def _1():
    """
    It copies all the files in a directory to another directory, and converts all the webp files to png files
    """
    dir     = '/Users/mark/Pictures/eyebleach'
    new_dir = '/Users/mark/Pictures/eyebleach new'
    files   = os.listdir(dir)
    os.makedirs(new_dir, exist_ok=True)

    exts       = ['.png', '.jpg', '.jpeg', '.mp4', '.webp']
    # exts_to_op = ['.png', '.jpg', '.jpeg']
    exts_to_op = ['.webp']

    for filename_ext in tqdm(files):
        # Check if its a cache file
        if filename_ext.startswith('.'):    continue

        # Get filename, extension, and filepath
        filename, ext = os.path.splitext(filename_ext)         # cannot use split('.') cz of vids being named "redditsave.com.---.mp4"
        filepath      = os.path.join(dir, filename_ext)

        # Check if its a file we want to copy
        if ext not in exts:                 continue

        # Check its a file we need to operate on
        if ext in exts_to_op:
            new_filepath = os.path.join(new_dir, f'{filename}.png')
            img          = Image.open(filepath)
            img.save(new_filepath)
        # Else, simply copies it
        else:
            new_filepath = os.path.join(new_dir, filename_ext)
            copy_file(filepath, new_filepath)

        # print(new_filepath)




_1()
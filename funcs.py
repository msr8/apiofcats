import random as r
import os

def get_file_path(eyebleach_path:str,
                  allowed_exts:list = ['png','jpg','jpeg','mp4'],
                  max_size = None) -> str:
    # Gets all the files and folders of the main directory where the pictures are stored
    all_files = os.listdir(eyebleach_path)
    # Loops thro them until it finds a valid file
    while True:
        # Selects a random file
        fname = r.choice(all_files)
        fp = os.path.join(eyebleach_path, fname)
        # Checks if its cache
        if fname.startswith('.'):    continue
        # Checks if its of a valid extension
        ext = os.path.splitext(fname)[1][1:]
        if not ext in allowed_exts:    continue
        # Checks if it satisfies the size limit
        size = os.path.getsize(fp)
        if not max_size == None:
            if size > max_size:    continue
        break

    return {'fp':fp, 'fname':fname, 'ext':ext, 'size':size}
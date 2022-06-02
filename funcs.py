import random as r
import os



def get_file_path(eyebleach_path:str,
                  allowed_exts:list = ['png','jpg','jpeg','mp4'],
                  max_size = None) -> str:
    # Gets all the files 
    all_files = os.listdir(eyebleach_path)
    # Shuffles them
    r.shuffle(all_files)
    # Loops thro them until it finds a valid file
    valid_file_found = False
    for fname in all_files:
        fp = os.path.join(eyebleach_path, fname)
        # Checks if its cache
        if fname.startswith('.'):      continue
        # Checks if its of a valid extension
        ext = os.path.splitext(fname)[1][1:]
        if not ext in allowed_exts:    continue
        # Checks if it satisfies the size limit
        size = os.path.getsize(fp)
        if not max_size == None:
            if size > max_size:        continue
        valid_file_found = True
        break

    if not valid_file_found:
        return None
    return {'fp':fp, 'fname':fname, 'ext':ext, 'size':size}



def process_arguments(request, DEFAULT_EXTS:list):
    # Gets all the args
    args              =  request.args
    ext               =  args.get('ext')
    max_size          =  args.get('max_size')
    redirect_arg      =  args.get('redirect')
    # Processes the arguments
    ext:list          =  ext.split(',') if ext else DEFAULT_EXTS
    max_size          =  int(max_size) if max_size else None
    redirect_arg:bool =  True if redirect_arg=='true' or redirect_arg=='True' else False
    # Returns the arguments
    return ext, max_size, redirect_arg








'''
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
'''


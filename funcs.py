import random as r
import os



def get_file_path(eyebleach_path:str,
                  allowed_exts:list = ['png','jpg','jpeg','mp4'],
                  max_size = None,
                  amount:int = 1) -> list:
    # Gets all the files 
    all_files = os.listdir(eyebleach_path)
    # Shuffles them
    r.shuffle(all_files)
    # Sets variables to use to determine the length of the loop
    valid_file_found = False
    file_count = 0
    files = []
    # Loops thro them until it finds a valid file
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
        # If it does, it sets valid_file_found to True and increases the file_count
        valid_file_found = True
        file_count += 1
        # Adds the file info to the list
        files.append({'fp':fp, 'fname':fname, 'ext':ext, 'size':size})
        # If the amount of files is reached, it breaks the loop
        if file_count >= amount:    break

    # If no valid file was found, returns None
    if not valid_file_found:    return None
    # Else, returns the list containing the info of the files
    return files



def process_arguments(request, DEFAULT_EXTS:list) -> tuple:
    # Gets all the args. Remember, URL args are given more priority than BODY args
    args              =  request.args if request.args else request.form
    ext               =  args.get('ext')
    max_size          =  args.get('max_size')
    redirect_arg      =  args.get('redirect')
    amount            =  args.get('amount')
    # Converts ints to string
    max_size, amount = str(max_size), str(amount)
    # Processes the arguments
    ext:list          =  ext.split(',') if ext else DEFAULT_EXTS
    max_size          =  int(max_size) if max_size.isdigit() else None
    redirect_arg:bool =  True if redirect_arg=='true' or redirect_arg=='True' else False
    amount:int        =  int(amount) if amount.isdigit() else 1
    # Returns the arguments
    return ext, max_size, redirect_arg, amount



def get_exts(eyebleach_path:str) -> dict:
    # Gets all the files and folders of the main directory where the pictures are stored
    all_stuff = os.listdir(eyebleach_path)
    # Loops thro them until it finds a valid file
    exts = {}
    for fname in all_stuff:
        # Checks if its cache
        if fname.startswith('.'):    continue
        # Gets its extension
        ext = os.path.splitext(fname)[1][1:]
        # Adds it to the dictionary
        if not ext in exts:    exts[ext] = 1
        else:                  exts[ext] += 1
    return exts







'''
def get_file_path(eyebleach_path:str,
                  allowed_exts:list = ['png','jpg','jpeg','mp4'],
                  max_size = None,
                  amount:int = 1) -> str:
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
'''


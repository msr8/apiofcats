from rich import print as printf

from   threading import Thread
import datetime  as dt
import random    as r
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
        if fname.startswith('.'):         continue
        # Checks if its of a valid extension
        ext = os.path.splitext(fname)[1][1:]
        if not ext in allowed_exts:       continue
        # Checks if its a video cache made by instagrapi/moviepy
        if fname.endswith('.mp4.jpg'):    continue
        # Checks if it satisfies the size limit
        size = os.path.getsize(fp)
        if not max_size == None:
            if size > max_size:           continue
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



def main_logme_func(req_dic:dict[str], log_dir:str, domain:str, extra:str=''):
    # Gets all the attributes
    ts      = get_ts()
    url     = req_dic['url'].replace(req_dic['host_url'], '')
    ip      = req_dic['access_route'][0]
    ref     = req_dic['referrer']
    log_fp  = os.path.join(log_dir, get_log_fp())
    # Enchancements
    ip  = ip  + ' ' * ( 15-len(ip) )
    url = url + ' ' * ( max( 10-len(url) , 0 ) ) 
    ext = f'{extra} '  if  extra                 else extra           # So that the logs are aligned when no extra is given
    ref = ''           if  domain in f'{ref}'    else ref
    ref = ''           if  not ref               else f'({ref}) '      
    # Generates the text
    text = f'[grey50][{ts}][/]  [blue3]{ip}[/] -- [magenta1]/{url}[/] [chartreuse4]{ref}[/]{ext}'
    # Prints it and saves to file
    printf(text)
    with open(log_fp, 'a') as f:
        f.write(f'{text}-- [light_steel_blue]{req_dic["user_agent"].string} {req_dic["accept_languages"].__str__()}[/]\n')
        # extra = extra.replace('[/]','').replace('[orange3]','')
        # f.write(f'[{ts}]  {ip}-- {ref}/{url} {extra} -- {request.user_agent.string} {request.accept_languages.__str__()}\n')



def logme(request, log_dir:str, domain:str, extra:str=''):
    req_dic = {
        'url':              request.url,
        'host_url':         request.host_url,
        'access_route':     request.access_route,
        'referrer':         request.referrer,
        'user_agent':       request.user_agent,
        'accept_languages': request.accept_languages
    }
    thr = Thread(target=main_logme_func, args=(req_dic, log_dir, domain, extra,))
    thr.start()



def get_ts() -> str:
    # Gets the current time
    timezone_diff = dt.timedelta(hours=5.5)  
    tz_info       = dt.timezone(timezone_diff, name="GMT")
    curr_time     = dt.datetime.now(tz_info)
    # Exracts all the attributes
    yr            = str(curr_time.year)[2:]
    mon           = str(curr_time.month).zfill(2)
    day           = str(curr_time.day).zfill(2)
    hr            = str(curr_time.hour).zfill(2)
    min           = str(curr_time.minute).zfill(2)
    sec           = str(curr_time.second).zfill(2)
    # Returns the string
    return f'{day}/{mon}/{yr} {hr}:{min}:{sec}'



def get_log_fp() -> str:
    # Gets the current time
    timezone_diff = dt.timedelta(hours=5.5)  
    tz_info       = dt.timezone(timezone_diff, name="GMT")
    curr_time     = dt.datetime.now()
    # Exracts all the attributes
    yr            = curr_time.year
    mon           = curr_time.month
    day           = curr_time.day
    # Returns the string
    return f'{yr}-{mon}-{day}.log'








'''



'''










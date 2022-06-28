import os
from PIL import Image
import requests as rq

def _1():
    allowed_exts:list = ['png','jpg','jpeg','mp4']
    max_size = 30*10**6
    all_files = os.listdir('/Users/ravi/Pictures/Eyebleach')

    all_valid = []

    for fname in all_files:
        fp = os.path.join('/Users/ravi/Pictures/Eyebleach', fname)

        # Checks if its cache
        if fname.startswith('.'):    continue
        # Checks if its of a valid extension
        ext = os.path.splitext(fname)[1][1:]
        if not ext in allowed_exts:    continue
        # Checks if it satisfies the size limit
        size = os.path.getsize(fp)
        if not max_size == None:
            if size > max_size:    continue
        
        all_valid.append(fname)

    # print('\n'.join(all_valid))

    print(f'\nTotal: {len(all_valid)}')



def _2():
    all_files = os.listdir('/Users/ravi/Pictures/Eyebleach')
    exts = {}
    for fname in all_files:
        if fname.startswith('.'):
            continue
        ext = os.path.splitext(fname)[1][1:]
        if not ext in exts:
            exts[ext] = 1
        else:
            exts[ext] += 1
    print(exts)



def _3():
    all_files = os.listdir('/Users/ravi/Pictures/Eyebleach')
    for fname in all_files:
        ext = os.path.splitext(fname)[1][1:]
        if ext == 'webp':
            # Convert it to png
            im = Image.open(os.path.join('/Users/ravi/Pictures/Eyebleach', fname))
            im.save(os.path.join('/Users/ravi/Pictures/Eyebleach', fname.replace('.webp', '.png')))
            # Delete the original
            os.remove(os.path.join('/Users/ravi/Pictures/Eyebleach', fname))
            # Log
            print(f'Converted {fname}')



def _4():
    url = 'http://127.0.0.1:5000/random'
    body = {'ext':'png'}
    r = rq.post(url, data=body)

    print(r.text)
    print(r.url)



def _5():
    fp = '/Users/ravi/Documents/Even_Newer_Python_Stuff/CATAPI/docs/test.html'
    with open(fp, 'r') as f:    text = f.read()
    text = text.replace('<', '&lt')
    text = text.replace('>', '&gt')
    text = text.replace('\n', '\n<br>')
    text = text.replace(' ', '&nbsp')
    # text = text.replace('"', '&quot')
    # text = text.replace('\'', '&apos')
    # text = text.replace('/', '&frasl')
    # text = text.replace('\\', '&frasl')
    # text = text.replace('(', '&#40')
    # text = text.replace(')', '&#41')
    # text = text.replace('[', '&#91')
    # text = text.replace(']', '&#93')
    # text = text.replace('{', '&#123')
    with open(fp, 'w') as f:    f.write(text)









_3()


# {'jpeg': 1470, 'mp4': 759, 'webp': 262, 'png': 78, '': 1, 'jpg': 4}
# {'jpeg': 1470, 'png': 340, 'mp4': 759, 'jpg': 4}




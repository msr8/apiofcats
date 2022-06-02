from flask import Flask, send_file, send_from_directory, redirect, url_for, render_template, request
from flask_restful import Api, Resource
from flask_restful import request as request_api

from funcs import get_file_path, process_arguments






EYEBLEACH_PATH = '/Users/ravi/Pictures/Eyebleach'
DOMAIN = 'http://127.0.0.1:5000'
DEFAULT_EXTS = ['png','jpg','jpeg','mp4']
app = Flask(__name__)
api = Api(app)














class Random(Resource):
    def get(self):
        # Gets all the args
        ext, max_size, _ = process_arguments(request, DEFAULT_EXTS)
        # Gets the file stuff
        file_dic = get_file_path(EYEBLEACH_PATH, ext, max_size)
        # Checks if the file was found
        if not file_dic:    return {'error':'No file found satisfying the given parameters'}, 301
        fname, ext, size = file_dic['fname'], file_dic['ext'], file_dic['size']
        dic = {
            'filename': fname,
            'url':      f'{DOMAIN}/library/{fname}',
            'ext':      ext,
            'size':     size
        }
        return dic
api.add_resource(Random, '/api/random')


@app.route('/')
def page_home():
    return 'Hello :)'


@app.route('/random')
def page_random():
    # Gets all the args
    ext, max_size, redirect_arg = process_arguments(request, DEFAULT_EXTS)
    # Gets the file
    try:       file_dic = get_file_path(EYEBLEACH_PATH, max_size=max_size, allowed_exts=ext)
    # If there is an error processing the arguments, shows error
    except:    file_dic = None
    # Checks if a file exists with the given parameters
    if not file_dic:    return send_file('static/error.jpg')
    # Gets the file info
    fp, fname, file_ext = file_dic['fp'], file_dic['fname'], file_dic['ext']
    # If the redirect arg is given, redirects
    if redirect_arg:    return redirect( url_for('page_library',fname=fname) )
    # Else, displays the media
    # return send_file(fp)
    html_file = 'video.html' if file_ext == 'mp4' else 'image.html'
    return render_template(html_file, fname=fname, url=f'{DOMAIN}/library/{fname}')


@app.route('/library/<fname>')
def page_library(fname):
    return send_from_directory(EYEBLEACH_PATH, fname)


@app.route('/test<arg1>')
def page_test(arg1):
    return render_template('photo.html', arg1=arg1)








if __name__ == '__main__':

    # from waitress import serve
    # serve(app, port=5000, host='0.0.0.0')
    
    app.run(debug=True)
    








'''
-> Add /stats
-> Fix download (in both, random AND library)
-> Add min size as a param
-> favicon.ico
-> Gets args in API

http://127.0.0.1:5000/library/ead9beic1jh71.jpeg
'''



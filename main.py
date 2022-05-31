from flask import Flask, send_file, send_from_directory, redirect, request
from flask_restful import Api, Resource
from flask_restful import request as request_api

from funcs import get_file_path






EYEBLEACH_PATH = '/Users/ravi/Pictures/Eyebleach'
DOMAIN = '127.0.0.1:5000'
DEFAULT_EXTS = ['png','jpg','jpeg','mp4']
app = Flask(__name__)
api = Api(app)














class Random(Resource):
    def get(self):
        args = request_api.args
        print(args)
        file_dic = get_file_path(EYEBLEACH_PATH)
        fname, ext, size = file_dic['fname'], file_dic['ext'], file_dic['size']
        dic = {
            'filename': fname,
            'url':      f'{DOMAIN}/library/{fname}',
            'ext':      ext,
            'size':     size
        }
        return dic


@app.route('/')
def page_home():
    return 'Hello :)'


@app.route('/random')
def page_random():
    # Gets all the args
    args =          request.args
    ext =           args.get('ext')
    max_size =      args.get('max_size')
    redirect_arg =  args.get('redirect')
    # Processes ext
    ext = ext.split(',') if ext else DEFAULT_EXTS
    # Gets the file info
    file_dic = get_file_path(EYEBLEACH_PATH, max_size=max_size, allowed_exts=ext)
    fp, fname = file_dic['fp'], file_dic['fname']
    # If the redirect arg is given, redirects
    if redirect_arg:    redirect(f'/library/{fname}')
    # Else, sends the file
    return send_file(fp)


@app.route('/library/<fname>')
def page_library(fname):
    return send_from_directory(EYEBLEACH_PATH, fname)







api.add_resource(Random, '/api/random')

if __name__ == '__main__':

    # from waitress import serve
    # serve(app, port=5000, host='0.0.0.0')
    
    app.run(debug=True)
    








'''
-> Fix download
-> Convert webp to png or smth
-> Add min size as a param
-> Add args input (in API)
-> favicon.ico
-> Change title to filename, or while saving
'''



from flask import Flask, send_file, send_from_directory, redirect, url_for, render_template, request
from flask_restful import Api, Resource
from flask_restful import request as request_api
from rich import print as printf

from funcs import get_file_path, process_arguments, get_exts
import os






EYEBLEACH_PATH = '/Users/ravi/Pictures/Eyebleach'
STATIC = os.path.join( os.path.dirname(__file__) , 'static' )
# EYEBLEACH_PATH = os.path.join( os.path.dirname(__file__) , 'Eyebleach' )
# DOMAIN = 'http://127.0.0.1:5000'
DOMAIN = 'https://7fbf-2401-4900-1c62-fff2-c22-1c93-dcb0-4d6a.in.ngrok.io'
DEFAULT_EXTS = ['png','jpg','jpeg','mp4']
app = Flask(__name__)
api = Api(app)

printf(f'[gray50][CONFIG] Eyebleach path:      [u]{EYEBLEACH_PATH}[/][/]')
printf(f'[gray50][CONFIG] Domain:              {DOMAIN}[/]')
printf(f'[gray50][CONFIG] Default extensions:  {", ".join(DEFAULT_EXTS)}[/]')













class Random(Resource):
    def get(self):
        # Gets the arguments
        ext, max_size, _, amount = process_arguments(request_api, DEFAULT_EXTS)
        # Gets the file stuff
        files = get_file_path(EYEBLEACH_PATH, ext, max_size, amount)
        # Checks if the file was found
        if not files:    return {'error':'No file found satisfying the given parameters'}
        # Goes thro the dictionaries present in the list, deletes all file paths, and adds URLs
        for dic in files:
            dic['url'] = f'{DOMAIN}/{dic["fname"]}'
            del dic['fp']
        # Returns the data
        return { 'amount':len(files) , 'files':files }
api.add_resource(Random, '/api/random')



class Stats(Resource):
    def get(self):
        # Gets the extensions
        exts = get_exts(EYEBLEACH_PATH)
        # Gets the number of total files
        total = sum(exts.values())
        # Returns the info
        return {
            'domain':      DOMAIN, 
            'filecount':   exts,
            'total_files': total
        }
api.add_resource(Stats, '/api/stats')



@app.route('/favicon.ico', methods=["GET", "POST"])
def favicon():
    return send_from_directory(STATIC, 'favicon.ico')



@app.route('/', methods=["GET", "POST"])
def page_home():
    return 'Hello :)'



@app.route('/random', methods=["GET", "POST"])
def page_random():
    # Gets all the args
    ext, max_size, redirect_arg, _ = process_arguments(request, DEFAULT_EXTS)
    print(request.args.get('ext'))
    print(request_api.form.get('ext'))
    print(ext)
    # Gets the file
    try:       file_dic = get_file_path(EYEBLEACH_PATH, max_size=max_size, allowed_exts=ext)[0]
    # If there is an error processing the arguments, shows error
    except:    file_dic = None
    # Checks if a file exists with the given parameters
    if not file_dic:    return send_from_directory(STATIC, 'error.jpg')
    # Gets the file info
    fp, fname, file_ext = file_dic['fp'], file_dic['fname'], file_dic['ext']
    # If the redirect arg is given, redirects
    if redirect_arg:    return redirect( url_for('page_library',fname=fname) )
    # Else, displays the media
    # return send_file(fp)
    html_file = 'video.html' if file_ext == 'mp4' else 'image.html'
    return render_template(html_file, fname=fname, url=f'/library/{fname}')
    return render_template(html_file, fname=fname, url=fp)


@app.route('/library/<fname>', methods=["GET", "POST"])
def page_library(fname):
    return send_from_directory(EYEBLEACH_PATH, fname)


@app.route('/test<arg1>')
def page_test(arg1):
    return render_template('photo.html', arg1=arg1)








if __name__ == '__main__':

    # from waitress import serve
    # serve(app, port=5000, host='0.0.0.0')
    
    app.run(debug=True, port=5000)
    








'''
-> Add /
-> Add /docs
-> Logging
-> Improve /stats
-> Add library exploring
-> Check if the max_size given is an int, and None

http://127.0.0.1:5000/library/ead9beic1jh71.jpeg
'''



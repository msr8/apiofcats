from flask         import Flask, send_file, send_from_directory, redirect, url_for, render_template, request
from flask_restful import request as request_api
from rich          import print as printf
from flask_restful import Api, Resource

from funcs import get_file_path, process_arguments, get_exts, logme

import json, os






app = Flask(__name__)
api = Api(app)




CONFIG_FP = os.path.join( os.path.dirname(__file__) , 'config.json' )
STATIC    = os.path.join( os.path.dirname(__file__) , 'static' )
# LOG_DIR = os.path.join( os.path.dirname(__file__) , 'logs' )
# LOG_FP  = os.path.join( LOG_DIR ,                    f'{int(t.time())}.txt' )
LOG_DIR   = os.path.join( os.path.dirname(__file__) , 'logs' )
DEFAULT_EXTS = ['png','jpg','jpeg','mp4']


# Loads config
with open(CONFIG_FP) as f:    CONFIG = json.load(f)
EYEBLEACH_PATH = CONFIG['eyebleach_path']
DOMAIN         = CONFIG['domain']

# Makes log dir
os.makedirs(LOG_DIR, exist_ok=True)
log_dir =   LOG_DIR

printf(f'[gray50][CONFIG] Eyebleach path:      [u]{EYEBLEACH_PATH}[/][/]')
printf(f'[gray50][CONFIG] Domain:              {DOMAIN}[/]')
printf(f'[gray50][CONFIG] Default extensions:  {", ".join(DEFAULT_EXTS)}[/]')
# printf(f'\n')













class Random(Resource):
    def func(self):
        # Gets the arguments
        ext, max_size, _, amount = process_arguments(request_api, DEFAULT_EXTS)
        # Gets the file stuff
        files = get_file_path(EYEBLEACH_PATH, ext, max_size, amount)
        # Checks if the file was found
        if not files:    return {'error':'No file found satisfying the given parameters'}
        # Goes thro the dictionaries present in the list, deletes all file paths, and adds URLs
        for dic in files:
            dic['url'] = f'{DOMAIN}/library/{dic["fname"]}'
            del dic['fp']
        # Logs it

        # Get the body args. If url args are given, dont print the body args. Then if no body args are given, prints an empty string
        args  = request_api.form
        extra = '' if request_api.args  else args.to_dict()
        extra = '' if not extra         else extra
        logme(request, log_dir, DOMAIN, extra)
        # Returns the data
        return { 'amount':len(files) , 'files':files }

    def get(self):     return self.func()
    def post(self):    return self.func()

api.add_resource(Random, '/api/random')



class Stats(Resource):
    def func(self):
        logme(request, log_dir, DOMAIN)
        # Gets the extensions
        exts = get_exts(EYEBLEACH_PATH)
        # Gets the number of total files
        total = sum(exts.values())
        # Returns the info
        return {
            'domain':      DOMAIN, 
            'total_files': total,
            'filecount':   exts,
        }

    def get(self):     return self.func()
    def post(self):    return self.func()

api.add_resource(Stats, '/api/stats')



@app.route('/favicon.ico', methods=["GET", "POST"])
def favicon():
    return send_from_directory(STATIC, 'favicon.ico')



@app.route('/', methods=["GET", "POST"])
def page_home():
    logme(request, log_dir, DOMAIN)
    exts = get_exts(EYEBLEACH_PATH)
    total = sum(exts.values())
    # return render_template('home.html', shit_to_be_filled_out_in_python=total, DOMAIN=DOMAIN)
    return render_template('home2.html', shit_to_be_filled_out_in_python=total, DOMAIN=DOMAIN)
    return 'Hello :)'



@app.route('/stats', methods=["GET", "POST"])
def page_stats():
    return Stats().func()



@app.route('/random', methods=["GET", "POST"])
def page_random():
    # Gets all the args
    ext, max_size, redirect_arg, _ = process_arguments(request, DEFAULT_EXTS)
    # Gets the file
    try:       file_dic = get_file_path(EYEBLEACH_PATH, max_size=max_size, allowed_exts=ext)[0]
    # If there is an error processing the arguments, shows error
    except:    file_dic = None
    # Checks if a file exists with the given parameters
    if not file_dic:    return send_from_directory(STATIC, 'error.jpg')
    # Gets the file info
    fp, fname, file_ext = file_dic['fp'], file_dic['fname'], file_dic['ext']
    # Logs it
    logme(request, log_dir, DOMAIN, f'[orange3]({fname})[/]')
    # If the redirect arg is given, redirects
    if redirect_arg:    return redirect( url_for('page_library',fname=fname) )
    # Else, displays the media
    html_file = 'video.html' if file_ext == 'mp4' else 'image.html'
    return render_template(html_file, fname=fname, url=f'/library/{fname}')



@app.route('/library/<fname>', methods=["GET", "POST"])
def page_library(fname):
    # logme(request)
    # print(request.user_agent)
    # print(type(request.user_agent))
    # print(request.user_agent.string)
    return send_from_directory(EYEBLEACH_PATH, fname)


@app.route('/test<arg1>')
def page_test(arg1):
    logme(request, log_dir, DOMAIN)
    return render_template('image.html', arg1=arg1)








if __name__ == '__main__':

    # from waitress import serve
    # serve(app, port=80, host='0.0.0.0')
    
    app.run(debug=True, port=80, host='0.0.0.0')
    # app.run()
    








'''
CODING BASED
-> Make the logme() func to save logs based on date
SERVER BASED
-> Change password of root and mark in server
-> Add keybased SSH authentication
LONG ASS SHIT
-> Add library exploring

-> Find if any file is 0 bytes



http://127.0.0.1/library/ead9beic1jh71.jpeg
'''



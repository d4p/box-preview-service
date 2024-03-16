from app import app
from flask import send_file, request
import subprocess
import os.path

@app.route('/')
@app.route('/index.html')
def index():
    #openscad -o test.png --imgsize=4096,4096  --colorscheme DeepOcean box_rounded.scad
    openscad_file = os.path.join(app.root_path,'..', 'openscad', 'box_rounded.scad')
    cache_file = os.path.join(app.root_path,'..', 'cache', 'box_rounded.png')
    return_code = subprocess.call(["openscad","-o",cache_file, "--imgsize=1024,1024", "--colorscheme", "DeepOcean", openscad_file])
    if return_code == 0:
        return 'Generated image'
    else:
        return 'Hello, World!' + str(return_code)
    
def parameters_validation(parameters):
    #allow only images between 100x100 and 4096x4096
    if int(parameters["image_size"]) > 4096 or int(parameters["image_size"]) < 100:
        print("image_size parameter error");
        return 0
    
    return 1

def parameters_to_file_name(parameters):
    #TODO: add real parameter parsing
    file_name = 'box_rounded_' + parameters["image_size"] +'.png'
    return file_name

def create_cache_filename(file):
    return os.path.join(app.root_path,'..', 'cache', file)

def check_cache(file):
    cache_file = create_cache_filename(file)
    if os.path.isfile(cache_file):
        return 1
    else:
        return 0

def generate_preview(parameters):
    file_name = parameters_to_file_name(parameters)
    cache_file = create_cache_filename(file_name)
    if (check_cache(file_name)):
        return cache_file
    else:
        openscad_file = os.path.join(app.root_path,'..', 'openscad', 'box_rounded.scad')
        return_code = subprocess.call(["openscad",
                                       "-o",
                                       cache_file, 
                                       "--imgsize=" + parameters["image_size"] + "," + parameters["image_size"],
                                       "--colorscheme", 
                                       "DeepOcean", 
                                       openscad_file])
        if return_code == 0:
            return cache_file
        else:   
            return 0

@app.route('/get_preview')
def get_preview():
    if request.args.get('type') == '1':
        filename = 'sample_file.png'
        imagetype = 'image/png'
    else:
        filename = '../resources/error.jpg'
        imagetype = 'image/jpg'
    return send_file(filename, mimetype=imagetype)

@app.route('/image.png')
def image():
    parameters = {
        "image_size": request.args["image_size"],
    }

    if parameters_validation(parameters) == 0:
        filename = '../resources/error.jpg'
        imagetype = 'image/jpg'
    else:
        filename = generate_preview(parameters)
        imagetype = 'image/png'
            
    return send_file(filename, mimetype=imagetype)

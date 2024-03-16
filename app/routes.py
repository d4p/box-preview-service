from app import app
from flask import send_file, request
import subprocess
import os.path

@app.route('/')

def parameters_validation(parameters):
    #allow only images between 100x100 and 4096x4096
    if int(parameters["image_size"]) > 4096 or int(parameters["image_size"]) < 100:
        print("image_size parameter error");
        return 0
    
    box_dimension_X = int(parameters["box_dimension_X"])
    box_dimension_Y = int(parameters["box_dimension_Y"])
    box_dimension_Z = int(parameters["box_dimension_Z"])

    if box_dimension_X < 30 or box_dimension_X > 250:
        print("box_dimesnion_X error")
        return 0
    if box_dimension_Y < 30 or box_dimension_Y > 250:
        print("box_dimesnion_Y error")
        return 0
    if box_dimension_Z < 30 or box_dimension_X > 280:
        print("box_dimesnion_Z error")
        return 0
    return 1

def parameters_to_file_name(parameters):
    #TODO: add real parameter parsing
    file_name = 'box_rounded_' + parameters["image_size"] + "bdx" + parameters["box_dimension_X"] + "bdy" + parameters["box_dimension_Y"] +"bdz" + parameters["box_dimension_Z"] + '.png'
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
                                       "-D", "box_dimension_X=" + parameters["box_dimension_X"] + "",  
                                       "-D", "box_dimension_Y=" + parameters["box_dimension_Y"] + "",
                                       "-D", "box_dimension_Z=" + parameters["box_dimension_Z"] + "",
                                       "--colorscheme", 
                                       "DeepOcean", 
                                       openscad_file])
        if return_code == 0:
            return cache_file
        else:   
            return 0

#positive test link http://127.0.0.1:5000/image.png?image_size=2222&box_dimension_X=150&box_dimension_Y=100&box_dimension_Z=150
@app.route('/image.png')
def image():
    parameters = {
        "image_size": request.args["image_size"],
        "box_dimension_X": request.args["box_dimension_X"],
        "box_dimension_Y": request.args["box_dimension_Y"],
        "box_dimension_Z": request.args["box_dimension_Z"],
    }

    if parameters_validation(parameters) == 0:
        filename = '../resources/error.jpg'
        imagetype = 'image/jpg'
    else:
        filename = generate_preview(parameters)
        imagetype = 'image/png'
            
    return send_file(filename, mimetype=imagetype)

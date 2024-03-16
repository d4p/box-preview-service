from app import app
from flask import send_file, request
import subprocess
import os.path
import hashlib


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
    
    wall_thickness = int(parameters["wall_thickness"])

    if wall_thickness < 1 or wall_thickness > 5:
        print("whall thicnkess error")
        return 0

    bottom_thickness = int(parameters["bottom_thickness"])
    if bottom_thickness < 2 or bottom_thickness > 10 or bottom_thickness > box_dimension_Z:
        print("bottom_thickness error")
        return 0
    
    round_radius = int(parameters["round_radius"])
    if round_radius < 0 or round_radius > (box_dimension_X/2) or round_radius > (box_dimension_Y/2):
        print("round_radius_error")
        return 0

    return 1

def parameters_to_file_name(parameters):
    #TODO: add real parameter parsing
    hash_object = hashlib.md5(str(parameters).encode())
    #file_name = 'box_rounded_' + parameters["image_size"] + "bdx" + parameters["box_dimension_X"] + "bdy" + parameters["box_dimension_Y"] +"bdz" + parameters["box_dimension_Z"] + '.png'
    file_name = 'box_rounded_' + hash_object.hexdigest() + '.png'
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
                                       "-D", "wall_thickness=" + parameters["wall_thickness"] + "",
                                       "-D", "bottom_thickness=" + parameters["bottom_thickness"] + "",
                                       "-D", "round_radius=" + parameters["round_radius"] + "",
                                       "--colorscheme", 
                                       "DeepOcean", 
                                       openscad_file])
        if return_code == 0:
            return cache_file
        else:   
            return 0

@app.route('/image.png')
def image():
    parameters = {
        "image_size": request.args["image_size"],
        "box_dimension_X": request.args["box_dimension_X"],
        "box_dimension_Y": request.args["box_dimension_Y"],
        "box_dimension_Z": request.args["box_dimension_Z"],
        "wall_thickness": request.args["wall_thickness"],
        "bottom_thickness": request.args["bottom_thickness"],
        "round_radius": request.args["round_radius"]
    }

    if parameters_validation(parameters) == 0:
        filename = '../resources/error.jpg'
        imagetype = 'image/jpg'
    else:
        filename = generate_preview(parameters)
        imagetype = 'image/png'
            
    return send_file(filename, mimetype=imagetype)

#!/bin/bash
#This script is called by docker. Runs the script that 
#starts the virtual framebuffer (required for openscad rendering) and runs the web app

./virtualfb.sh
export DISPLAY=:128
gunicorn --bind 0.0.0.0:5000 app:app
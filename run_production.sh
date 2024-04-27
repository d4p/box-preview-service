#!/bin/bash
#This script is called by docker. Runs the script that 
#starts the virtual framebuffer (required for openscad rendering) and runs the web app

./virtualfb.sh
export DISPLAY=:128

#dirty hack for cache, it will fail if the folder already exist
mkdir cache

gunicorn --log-file ./log.log -t 300 --threads 2 --bind 0.0.0.0:5000 app:app

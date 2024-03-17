#!/bin/bash

./virtualfb.sh
export DISPLAY=:128
gunicorn --bind 0.0.0.0:5000 app:app
#lets use ubuntu image to run the appication, we need this to easy setup flask and openscad
FROM ubuntu:22.04

#update package list
RUN apt-get update

#not sure if this is right place
WORKDIR /app

#copy all the files to the container
COPY . .

#instll ubuntu dependencies
#RUN apt-get install -y < requirements_ubuntu.txt
RUN xargs apt-get install -y < requirements_ubuntu.txt

COPY ./openscad/box_black.json /usr/share/openscad/color-schemes/render/
COPY ./openscad/box_white.json /usr/share/openscad/color-schemes/render/

#install python dependencies
RUN pip install --no-cache-dir -r requirements_python.txt

EXPOSE 5000

#TODO run production server instead fo flask
CMD ["flask", "run"]

#TODO add two stage docker to save time on image building
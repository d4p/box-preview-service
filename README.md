# box-preview-service
Sample usage 
#preview generation example
http://127.0.0.1:5000/image.png?image_size=2223&box_dimension_X=150&box_dimension_Y=100&box_dimension_Z=150&wall_thickness=4&bottom_thickness=3&round_radius=30&hole_diameter=20&hole_Z=80&color=bb

#stl file generation example
http://127.0.0.1:5000/box.stl?image_size=2223&box_dimension_X=150&box_dimension_Y=100&box_dimension_Z=150&wall_thickness=4&bottom_thickness=3&round_radius=30&hole_diameter=20&hole_Z=80&color=bb

#run application
flask run


#Docker build image (2 stage)
#run as root
docker build --no-cache -f ubuntu_ready.Dockerfile --tag="ubuntu_ready" .

docker build -f production.Dockerfile --tag="production_box_preview" .

docker run --network="host" production_box_preview





#Docker build image - old way with single dockerfile, downloads all dependencies every time
sudo docker build -f ubuntu_ready.Dockerfile --tag "preview_generator" .

#Docker run locally
docker run --network="host" preview_generator


#make docker-clean;)
docker system prune -f

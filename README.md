# box-preview-service
Sample usage 

http://127.0.0.1:5000/image.png?image_size=2223&box_dimension_X=150&box_dimension_Y=100&box_dimension_Z=150&wall_thickness=4&bottom_thickness=3&round_radius=30&hole_diameter=20&hole_Z=40

#run application
flask run

#Docker build image
sudo docker build --tag "preview_generator" .

#Docker run locally
docker run -p 5000:5000 --network="host" preview_generator

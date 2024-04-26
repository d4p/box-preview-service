FROM ubuntu_ready

#not sure if this is right place
WORKDIR /app

#copy all the files to the container
COPY . .

EXPOSE 5001

#CMD ["flask", "run"]
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
CMD ["./run_production.sh"]

#TODO add two stage docker to save time on image building
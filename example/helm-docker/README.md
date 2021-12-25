# Custom-exporter Project

This project creates an HTTP Server as docker container that listens on a specified port and gathers/serves the metrics 


**Execute installation with docker-compose**
```sh
cd example/helm-docker/compose
docker-compose up --build
```

**Execute installation with helm**
```sh
cd example/helm-docker/app
docker build . -t kloia/custom-exporter:0.1
cd ../helm
helm install custom-exporter . --set service.port=9000
```
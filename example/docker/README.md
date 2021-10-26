# Custom-exporter Project

This project creates an HTTP Server as systemd service that listens on a specified port and gathers/serves the metrics 

**Execute installation with ansible-playbook**
```sh

docker compose 

git clone https://github.com/kloia/prometheus-custom-exporter
cd prometheus-custom-exporter
docker-compose up --build
```
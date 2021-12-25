# Custom-exporter Project

This project creates an HTTP Server as systemd service that listens on a specified port and gathers/serves the metrics 

**Execute installation with ansible-playbook**
```sh

cd example/ansible
ansible-playbook -i hosts.ini application_exporters.yaml
```
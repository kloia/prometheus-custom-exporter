FROM python:3.6

RUN /usr/local/bin/python -m pip install git+https://github.com/kloia/prometheus-custom-exporter

ENTRYPOINT [ "python3"]
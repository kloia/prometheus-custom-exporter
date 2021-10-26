FROM python:3.6

ARG PORT=9000
RUN /usr/local/bin/python -m pip install git+https://github.com/kloia/prometheus-custom-exporter

WORKDIR /app

COPY . .

ENTRYPOINT [ "python3", "/app/exporter.py" ]

EXPOSE ${PORT}
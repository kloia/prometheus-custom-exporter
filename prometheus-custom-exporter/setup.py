import setuptools

setuptools.setup(
    name='cexporter',
    version='0.0.1',
    author='Muhammed Kaya',
    author_email='muhammed@kloia.com',
    description='Prometheus custom exporter module for Python',
    long_description='Prometheus custom exporter module for Python',
    long_description_content_type="text/markdown",
    packages=['cexporter'],
    install_requires=['requests==2.25.1', 'prometheus_client==0.9.0', 'configparser'],
)

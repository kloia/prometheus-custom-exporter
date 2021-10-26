import requests
import socket
import logging
import os


class Service():

    @staticmethod
    def check_service_status_by_ports(host, ports):
        """Checks socket connections on specified ports and returns the status of service

        Args:
            host (str): Hostname
            ports (list(int)): Port numbers

        Returns:
            int : The status of service. 1 for active, 0 for inactive

        Usage Example:
            Service.check_service_status_by_ports('127.0.0.1', ['80', '8080'])
        """
        status = False
        for port in ports:
            status = Service.check_socket_connection(host, port)
            if status is True:
                logging.info("Port {} is open".format(port))
            else:
                break
        return 1 if status is True else 0

    @staticmethod
    def check_socket_connection(host, port):
        """Checks socket connection on a specified port

        Args:
            host (str): Hostname
            ports (int): Port number

        Returns:
            bool : The status of socket connection. True for active, False for inactive

        Usage Example:
            Service.check_socket_connection('127.0.0.1', '80')
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((host, port))
        s.close()
        return result == 0

    @staticmethod
    def check_service_status_by_http_endpoint(url, verify=False):
        """Sends a request to specified endpoint and returns the status of service as a metric

        Args:
            url (str): Endpoint
            verify (int)(Optional): Verifies https requests
                - default: False

        Returns:
            int : The status of service. 1 for active, 0 for inactive

        Usage Example:
            Service.check_service_status_by_http_endpoint('www.google.com')
            Service.check_service_status_by_http_endpoint('www.google.com', verify=False)
            Service.check_service_status_by_http_endpoint('www.google.com', verify=True)
        """
        try:
            response = requests.get(url=url, verify=verify)
            if response.ok:
                status = 1
            else:
                status = 0
        except Exception as exp:
            logging.error(exp)
            status = 0
        return status

    @staticmethod
    def get_host():
        """Gets host by hostname and returns it

        Args:

        Returns:
            str : Host

        Usage Example:
            Service.get_host()
        """
        hostname = Service.get_hostname()
        host = socket.gethostbyname(hostname)
        return host

    @staticmethod
    def get_hostname():
        """Gets hostname and returns it

        Args:

        Returns:
            str : Hostname

        Usage Example:
            Service.get_hostname()
        """
        return socket.gethostname()

    @staticmethod
    def check_service_status_by_bash_command(command, unexpectedOutput=[]):
        """Runs a bash command and returns output of the command as status of service

        Args:
            command (str): Bash command to query the status of the service.
            unexpectedOutput (list)(Optional): The list which includes unexpected outputs of bash command.
                - default: []

        Returns:
            int : The status of service. 1 for active, 0 for inactive

        Usage Example:
            Service.check_service_status_by_bash_command('kubectl get nodes --no-headers | wc -l')
            Service.check_service_status_by_bash_command('kubectl get nodes --no-headers | wc -l', [1])
        """
        result = None
        try:
            output = os.popen(command).read()
            result = 0 if any(map(lambda x: x == output, unexpectedOutput)) else 1
        except Exception as exp:
            logging.error(exp)
            result = 0
        return result

import os
import logging
from kloia_exporter.service import Service
import requests
import json


class MetricService(Service):

    @staticmethod
    def get_metrics_by_endpoint(url, verify=False):
        """Sends a request to specified endpoint and returns the response as a metric

        Args:
            url (str): Endpoint
            verify (bool)(Optional): Verifies https requests
                - default: False

        Returns:
            int/str/float : The return type is not clear since we don't know what type of data
            endpoint will return for successfull gathering, 0 otherwise

        Usage Example:
            MetricService.get_metrics_by_endpoint('www.google.com')
            MetricService.get_metrics_by_endpoint('www.google.com', verify=False)
            MetricService.get_metrics_by_endpoint('www.google.com', verify=True)
        """
        try:
            metricResult = requests.get(url, verify=verify)
        except requests.exceptions.ConnectionError:
            return 0

        if metricResult.ok:
            metric = metricResult.content
        else:
            metric = 0

        return metric

    @staticmethod
    def get_metrics_by_bash_command(command):
        """Runs a bash command and returns output of the command as a metric

        Args:
            command (str): Bash command to query metric

        Returns:
            float : Numerical value for success, 0 otherwise

        Usage Example:
            MetricService.get_metrics_by_bash_command('kubectl get nodes --no-headers | wc -l')
        """
        metric = None
        try:
            metric = os.popen(command).read()
        except Exception as exp:
            logging.error(exp)
            metric = 0

        try:
            metric = float(metric)
        except Exception as exp:
            logging.error(exp)
            metric = 0
        return metric

    @staticmethod
    def get_metrics_by_bash_script(script, outputFile=None, expectedKey=None):
        """Runs a bash script and returns output of script as a metric

        Args:
            command (str): Bash command to query the status of the service.
            outputFile (str): The file to which the output of the running script is written should be named so that this file can be read as json.
                - default: None
            expectedKey (str): The key to be obtained from output file.
                - default: None

        Returns:
            float : Numerical value for success, 0 otherwise

        Usage Example:
            Case 1:
                It runs a shell script and returns the output of script.

                MetricService.get_metrics_by_bash_script('get_total_users.sh')

           Case 2:
                If outputFile parameter is given then script creates and writes the output to the json file,
                with expectedKey parameter, metric can be gathered from json file

                MetricService.get_metrics_by_bash_script('get_user.sh 1', 'user_1.json', 'username')

                - get_user.sh 1 , runs script and writes the output to user_1.json.
                - user_1.json file is read and gathered expectedKey value.
        """
        try:
            script_output = os.popen(script)
        except Exception as exp:
            logging.error(exp)
            return 0
        if outputFile is None:
            return script_output.read()
        result = File.read_file_and_get_json_body(outputFile)
        return 0 if expectedKey not in result else result[expectedKey]


class File():

    @staticmethod
    def read_file_and_get_json_body(fileName):
        """Reads the json file and returns the content of the file

        Args:
            fileName (str): Name of the json file

        Returns:
            dict : Content of the json file

        Usage Example:
            File.read_file_and_get_json_body('users.json')
        """
        json_data = dict()
        try:
            with open(fileName, "r") as file:
                data = file.read()
                json_data = json.loads(data)
        except Exception as exp:
            logging.error(exp)
        return json_data

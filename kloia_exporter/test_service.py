from unittest import mock, TestCase
from kloia_exporter.service import Service


class TestService(TestCase):

    @mock.patch("kloia_exporter.service.Service.check_socket_connection", side_effect=[True, False])
    def test_check_service_status_by_ports_when_one_port_down_others_up_expected_error(self, mock_socket_func):
        host = "host"
        ports = [7550, 7551]
        result = Service.check_service_status_by_ports(host, ports)
        self.assertEqual(0, result)
        calls = [mock.call(host, port) for port in ports]
        mock_socket_func.assert_has_calls(calls)

    @mock.patch("kloia_exporter.service.Service.check_socket_connection", side_effect=[True, True])
    def test_check_service_status_by_ports_when_all_ports_up_expected_success(self, mock_socket_func):
        host = "host"
        ports = [7550, 7551]
        result = Service.check_service_status_by_ports(host, ports)
        self.assertEqual(1, result)
        calls = [mock.call(host, port) for port in ports]
        mock_socket_func.assert_has_calls(calls)

    @mock.patch("kloia_exporter.service.Service.check_socket_connection", side_effect=[False, False])
    def test_check_service_status_by_ports_when_all_ports_down_expected_error(self, mock_socket_func):
        host = "host"
        ports = [7550, 7551]
        result = Service.check_service_status_by_ports(host, ports)
        self.assertEqual(0, result)
        mock_socket_func.assert_called_once()

    @mock.patch('socket.socket.connect_ex', return_value=0)
    def test_check_socket_connection_when_socket_open_expected_success(self, mock_socket_connection):
        result = Service.check_socket_connection("hostname", "port")
        self.assertEqual(True, result)
        mock_socket_connection.assert_called_once()

    @mock.patch('socket.socket.connect_ex', return_value=500)
    def test_check_socket_connection_when_socket_close_expected_error(self, mock_socket_connection):
        result = Service.check_socket_connection("hostname", "port")
        self.assertEqual(False, result)
        mock_socket_connection.assert_called_once()

    @mock.patch("requests.get", return_value=mock.Mock(**{"ok": True}))
    def test_check_service_status_by_http_endpoint_when_service_up_expected_success(self, mock_request):
        url = "https: //localhost/path?key=key"
        status = Service.check_service_status_by_http_endpoint(url)
        self.assertEqual(1, status)
        mock_request.assert_called_once()

    @mock.patch("requests.get", return_value=mock.Mock(**{"ok": False}))
    def test_check_service_status_by_http_endpoint_when_service_down_expected_error(self, mock_request):
        url = "https: //localhost/path?key=key"
        status = Service.check_service_status_by_http_endpoint(url)
        self.assertEqual(0, status)
        mock_request.assert_called_once()

    @mock.patch('socket.gethostname', return_value='hostname')
    def test_get_hostname(self, mock_hostname):
        self.assertEqual("hostname", Service.get_hostname())
        mock_hostname.assert_called_once()

    @mock.patch('socket.gethostname', return_value='hostname')
    @mock.patch('socket.gethostbyname', return_value='host')
    def test_get_host(self, mock_host, mock_hostname):
        self.assertEqual("host", Service.get_host())
        mock_hostname.assert_called_once()
        mock_host.assert_called_once()

    @mock.patch("os.popen", return_value=mock.Mock(**{"read.return_value": "Active running"}))
    def test_check_service_status_by_bash_command_when_not_unexpected_output__expected_service_up(self, mock_command):
        unexpectedOuput = ["", " ", None]
        self.assertEqual(1, Service.check_service_status_by_bash_command(""" systemctl status httpd|grep "Active: active (running)" """, unexpectedOuput))
        mock_command.assert_called_once()

    @mock.patch("os.popen", return_value=mock.Mock(**{"read.return_value": ""}))
    def test_check_service_status_by_bash_command_when_unexpected_output_expected_service_down(self, mock_command):
        unexpectedOuput = ["", " ", None]
        self.assertEqual(0, Service.check_service_status_by_bash_command(""" systemctl status httpd|grep "Active: active (running)" """, unexpectedOuput))
        mock_command.assert_called_once()

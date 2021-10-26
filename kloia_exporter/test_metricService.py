from unittest import mock, TestCase
from kloia_exporter.metricService import MetricService


class TestMetricService(TestCase):

    @mock.patch("requests.get", return_value=mock.Mock(**{"ok": True, "content": 1}))
    def test_get_metrics_by_endpoint_when_response_http_status_200(self, mock_request):
        url = "https://localhost:3000/health"
        self.assertEqual(1, MetricService.get_metrics_by_endpoint(url))
        mock_request.assert_called_once()

    @mock.patch("requests.get", return_value=mock.Mock(**{"ok": False}))
    def test_get_metrics_by_endpoint_when_response_http_status_not_200(self, mock_request):
        url = "https://localhost:3000/health"
        self.assertEqual(0, MetricService.get_metrics_by_endpoint(url))
        mock_request.assert_called_once()

    @mock.patch("os.popen", return_value=mock.Mock(**{"read.return_value": 1}))
    def test_get_metrics_by_bash_command_when_command_success(self, mock_metric):
        command = "sudo kubectl get node | wc -l"
        self.assertEqual(1, MetricService.get_metrics_by_bash_command(command))
        mock_metric.assert_called_once()

    @mock.patch("os.popen", return_value=mock.Mock(**{"read.side_effect": Exception("command raises error")}))
    def test_get_metrics_by_command_when_command_raises_error(self, mock_metric):
        command = "sudo kubectl get node | wc -l"
        self.assertEqual(0, MetricService.get_metrics_by_bash_command(command))
        mock_metric.assert_called_once()

    @mock.patch("os.popen", return_value=mock.Mock(**{"read.return_value": "string"}))
    def test_get_metrics_by_command_when_response_not_float(self, mock_metric):
        command = "sudo kubectl get node | wc -l"
        self.assertEqual(0, MetricService.get_metrics_by_bash_command(command))
        mock_metric.assert_called_once()

from unittest import mock, TestCase
from kloia_exporter.metricInput import MetricInput, Metric
from kloia_exporter.collector import Collector

dummy_data = {
    "metric_inputs": [
        MetricInput(
            metricName="metricName",
            helpText="helpText",
            labels=["labelKey"],
            metrics=[Metric(["labelValue"], 10)]
        )
    ]
}


class TestCollector(TestCase):

    collector = None

    @classmethod
    @mock.patch('kloia_exporter.metricService.MetricService.get_host', return_value="localhost")
    def setUpClass(cls, mock_host):
        cls.mock_host = mock_host
        cls.mock_host.start()
        cls.collector = Collector(dummy_data["metric_inputs"])

    @classmethod
    def tearDownClass(cls):
        cls.mock_host.stop()
        cls.collector = None

    @mock.patch('kloia_exporter.collector.Collector.collect')
    def test_collect_func(self, mock_collect_func):
        mock_collect_func.return_value = True
        result = TestCollector.collector.collect()
        self.assertEqual(True, result)
        mock_collect_func.assert_called_once()

    def test_collect(self):
        result = list(TestCollector.collector.collect())
        self.assertEqual(1, len(result))
        self.assertEqual(10, result[0].samples[0].value)

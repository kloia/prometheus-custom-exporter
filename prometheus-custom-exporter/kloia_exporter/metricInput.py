from prometheus_client.core import GaugeMetricFamily


class MetricInput():

    def __init__(self, metricName, helpText, labels, metrics=[]):
        self.metricName = metricName
        self.helpText = helpText
        self.labels = labels
        self.metrics = metrics

    def get_metric(self):
        metricFamily = GaugeMetricFamily(self.metricName, self.helpText, labels=self.labels)
        for metric in self.metrics:
            metric.add_to_metric_family(metricFamily)
        return metricFamily


class Metric():

    def __init__(self, labelValues, value):
        self.labelValues = labelValues
        self.value = value

    def add_to_metric_family(self, metricFamily):
        metricFamily.add_metric(self.labelValues, self.value)

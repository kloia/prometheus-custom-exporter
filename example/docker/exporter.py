#!/usr/bin/env python
from kloia_exporter import API

metric_inputs = [
    {
        "metricName": "metricName",
        "helpText": "helpText",
        "labels": ["labelKey"],
        "collect": lambda metricFamily: metricFamily.add_metric( ["labelValue"], 10 )
    }
]

API(9000, metric_inputs=metric_inputs).listen()

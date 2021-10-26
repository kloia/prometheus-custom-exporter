#!/usr/bin/env python
from kloia_exporter import API, MetricInput, Metric
import os

metric_inputs = [
    MetricInput(
        metricName="metricName",
        helpText="helpText",
        labels=["labelsKey"],
        metrics=[
            Metric(
                labelValues=["labelValue"],
                value=10
            )
        ]
    )
]

API(int(os.environ.get('PORT')), metric_inputs=metric_inputs).listen()

#!/usr/bin/env python
from shared import API, MetricInput, Metric

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

API(9000, metric_inputs=metric_inputs).listen()

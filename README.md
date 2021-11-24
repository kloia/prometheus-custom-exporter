# Prometheus Custom Exporter Pip Package

`kloia_exporter` aims to provide simple and efficient solutions to create custom exporters which target Prometheus. It is the pip package that can be used to create REST API and yield metrics.

# Installation
```
pip3 install git+https://github.com/kloia/prometheus-custom-exporter
```

# Usage
Define a list that includes Python dicts. These objects must contain some keys metricName, helpText, labels, and the collect lambda function.  By defining a collect function, Prometheus Client calls it and yields the metric from the port. 

```Python
from kloia_exporter import API

metric_inputs = [
    {
        "metricName": "totalUsers",
        "helpText": "Number of total users",
        "labels": ["totalUsers"],
        "collect": lambda metricFamily: metricFamily.add_metric(["kloia"], 10 )
    }
]

API(9000, metric_inputs=metric_inputs).listen()
```

# Examples

## Example 1 - Custom Exporter for Couchbase Metrics 

There is  a requirement to be able to develop a custom exporter for Couchbase Metrics. Install the Couchbase Python SDK. 

```
pip3 install git+https://github.com/kloia/prometheus-custom-exporter
pip3 install couchbase
```

### Step 1 - Create `exporter.py`

Here is the script to help you develop a custom exporter.

```Python
from kloia_exporter import API, config
from data_layer import DataLayer

couchbase_config = config.get_config_info("service_check.ini", "couchbase")

dao = DataLayer(couchbase_config)

metric_inputs = [
   {
       "metricName": "totalUsers",
       "helpText": "Total Users",
       "labels": ["totalUsers"],
       "collect": lambda metricFamily: 
                      metricFamily.add_metric( 
                         ["totalUsers"],
                         dao.get(“select count(*) from Kloia”)[0][“$1”]   

                      )
   },
   {
       "metricName": "totalUsersByStartDate",
       "helpText": "Total Users By Start Date",
       "labels": ["totalUsersByStartDate"],
       "collect": lambda metricFamily: 
                      metricFamily.add_metric( 
                         ["totalUsersByStartDate"],
                         dao.get('select count(*) from Kloia AS doc WHERE doc.start_date < "24-11-2021"')[0][“$1”]   

                      )
   }
]

API(int(couchbase_config["port_number"]), metric_inputs=metric_inputs).listen()
```

### Step 2 - Create data_layer.py

Here is the script to connect Couchbase Server by using Couchbase Python SDK.  Give the credentials on service_check.ini,  as a parameter to the DataLayer object on the `exporter.py.` It will create a connection. This will allow you to get metrics by writing N1QL queries.


```Python
from couchbase.cluster import Cluster
from couchbase.auth import PasswordAuthenticator
import logging

class DataLayer():

   def __init__(self, args):
       self.args = args
       try:
           self.cluster = self.__connect_db()
           self.bucket = self.cluster.bucket("Kloia")
           self.collection = self.bucket.default_collection()
       except Exception as exp:
           logging.error(exp)

   def __get_authenticator(self):
       if self.args["user_name"] and self.args["password"]:
           return PasswordAuthenticator(self.args["user_name"], self.args["password"])
       return None

   def __get_conn_str(self):
       if self.args["cluster"]:
           return "couchbase://" + self.args["cluster"]
       return None

   def __connect_db(self):
       try:
           authenticator = self.__get_authenticator()
           conn_str = self.__get_conn_str()
           return Cluster(conn_str, authenticator=authenticator)
       except Exception as exp:
           logging.error(exp)
       return None

   def get(self, queryprep):
       try:
           res = self.cluster.query(queryprep)
           return res.rows()
       except Exception as exp:
           logging.error(exp)
           return []
```

### Step 3 - Create service_check.ini

The config file is as follows. It includes the Prometheus client’s port number and some credentials for connecting to the Couchbase Server. These fields must be updated before running `exporter.py.`

```
[couchbase]
port_number={{couchbase_exporter_port_number}}
cluster={{couchbase_exporter_cluster}}
user_name={{couchbase_user_name}}
password={{couchbase_password}}
```
### Step 4 - Run the `exporter.py`
The custom exporter will be ready on the specified port.

```Shell
python3 exporter.py
``` 
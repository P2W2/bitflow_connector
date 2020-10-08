# bitflow_connector
This project provides an infrastructure to get historical and live metrics from different monitoring tools and forward them to the TU-Berlin AIOps operation system.
The data is received from different sources in a various formats and converted to the Bitflow-CVS format to forwarded it in the AIOps data chain.

# Configuration
The main configuration file lies in ```\settings\configuration.yml```. 
```
# Incoming streams from rieman servers or clients. Input is received as protobuf messages.
riemann_stream:
  # Local Adress
  host: "localhost"
  port: 1234
  # Incoming metrics that will be forwarded as bitflow-format. If this not set all metrics will be forwarded.
  metrics: ['cpu_usage', 'memory_usage']
  # Names of AIOps instances to which the previously defined metrics are sent. Names are specified in destination_configs. 
  metric_destinations: [remote_host, my_machine]

# This sections shows the configuration to scrape metrics from the riemann index.
riemann_index:
# targets addresses of riemann instances
  targets:
    - host: localhost
      port: 12345
      scrape_interval: 5000
  # Metrics that will be queried and forwarded as bitflow-format. If this not set all metrics will be queried and forwarded.
  metrics: ['bla1', 'bla2']
  # Names of AIOps instances to which the previously defined metrics are sent. Names are specified in destination_configs.
  metric_destinations: ['bl1', 'bl2']
  # On the first connection a query is used to get historical data. Define how old this data can be. Is not set no historical data will be queried.
  historical: '3d'
  
# This sections shows the configuration to scrape prometheus targets directly
prometheus:
  # targets addresses
  targets:
    - host: 'localhost
      port: '5000'
      # used protocol http or https
      protocol: http
      # path to the published metrics
      path: '\metrics'
      # scrape interval  in seconds. 
      scrape_interval: 5
  # Metrics that will be queried and forwarded as bitflow-format. If this not set all metrics will be queried and forwarded.
  metrics: ['cpu_usage', 'disk_usage']
  # Names of AIOps instances to which the previously defined metrics are sent. Names are specified in destination_configs. 
  metric_destinations: [my_machine]
  
  # This sections shows the configuration to scrape metrics from the prometheus API.
  prometheus_ql:
  # targets addresses of prometheus instances
  targets:
    - host: localhost
      port: 12345
      scrape_interval: 5000
  # Metrics that will be queried and forwarded as bitflow-format. If this not set all metrics will be queried and forwarded.
  metrics: ['bla1', 'bla2']
  # Names of AIOps instances to which the previously defined metrics are sent. Names are specified in destination_configs.
  metric_destinations: ['bl1', 'bl2']
  # On the first connection a query is used to get historical data. Define how old this data can be. Is not set no historical data will be queried.
  historical: '3d'
  
destination_configs:
 # Destionation adresses of AIOps instances 
  - name: my_machine
    host: localhost
    port: 6000
  - name: remote_host
    host: 123.1.1.100
    port: 4999
```
# Docker
```
docker run -v /path/to/configuration/file.yml:/settings/configuration.yml p2w2/bitflow_connector
```


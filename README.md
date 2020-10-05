# bitflow_connector
This project provides an infrastructure to get historical and live metrics from different monitoring tools and forward them to the TU-Berlin AIOps operation system.
The data is received from different sources in a various formats and converted to the Bitflow-CVS format to forwarded it in the AIOps data chain.

# RUN
The project bases on Docker. The main configuration file lies in ```\settings\configuration.yml```. 
```
#incoming streams from rieman servers or clients. Input is received as protobuf messages.
riemann_stream:
  host: 
  port: 
  # incoming metrics that will be forwarded as bitflow-format. If this not set all metrics will be forwarded.
  metrics: []
  metric_destinations: []
prometheus:
  type: prometheus
  targets:
    - host: 
      port: 
      path: 
      scrape_interval: 
  metrics: []
  metric_destinations: []
destination_configs:
  - name: 
    host: 
    port: 
```

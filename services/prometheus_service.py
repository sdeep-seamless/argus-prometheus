from prometheus_api_client import PrometheusConnect

from config.settings import (
    PROMETHEUS_URL
)

prom = PrometheusConnect(
    url=PROMETHEUS_URL,
    disable_ssl=True
)

class PrometheusService:

    def get_cpu_usage(self):

        query = """
        100 -
        (
          avg by(instance)
          (
            rate(
             node_cpu_seconds_total{
              mode="idle"
             }[5m]
            )
          ) * 100
        )
        """

        return prom.custom_query(query)

    def get_memory_usage(self):
    
        query = """
        (
          1 -
          (
            node_memory_MemAvailable_bytes
            /
            node_memory_MemTotal_bytes
          )
        ) * 100
        """
    
        return  prom.custom_query(query)
    
    

    def get_network_usage(self):
    
        query = """
        sum by(instance)
        (
          rate(
            node_network_receive_bytes_total[5m]
          )
          +
          rate(
            node_network_transmit_bytes_total[5m]
          )
        )
        """
    
        return prom.custom_query(query)

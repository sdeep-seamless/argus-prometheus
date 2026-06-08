### A Distilled and hack implementation of Elasticsearch RemoteWite

ES Index for metrics
-----------------
curl -X PUT "http://10.91.10.154:9200/argus-metrics" \
-H "Content-Type: application/json" \
-d '{
  "mappings": {
    "properties": {
      "@timestamp": {
        "type": "date"
      },
      "instance": {
        "type": "keyword"
      },
      "metric": {
        "type": "keyword"
      },
      "type": {
        "type": "keyword"
      },
      "value": {
        "type": "float"
      },
      "mean": {
        "type": "float"
      },
      "std": {
        "type": "float"
      },
      "z_score": {
        "type": "float"
      }
    }
  }
}'

ES Index for alerts
-------------------
curl -X PUT "http://10.91.10.154:9200/argus-alerts" \
-H "Content-Type: application/json" \
-d '{
  "mappings": {
    "properties": {
      "@timestamp": {
        "type": "date"
      },
      "instance": {
        "type": "keyword"
      },
      "metric": {
        "type": "keyword"
      },
      "type": {
        "type": "keyword"
      },
      "value": {
        "type": "float"
      },
      "mean": {
        "type": "float"
      },
      "std": {
        "type": "float"
      },
      "z_score": {
        "type": "float"
      }
    }
  }
}'

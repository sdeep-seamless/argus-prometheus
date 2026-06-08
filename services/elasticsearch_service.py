from elasticsearch import Elasticsearch

from config.settings import ELASTIC_URL


class ElasticsearchService:

    def __init__(self):

        self.client = Elasticsearch(ELASTIC_URL)

    def save_metric(
        self,
        document
    ):
        try:
            self.client.index(index="argus-metrics",document=document)
        except Exception as e:
            print(f"[ES ERROR] {e}")

        return self.client.index(index="argus-metrics",document=document)

    def save_alert(
        self,
        document
    ):
        try:
            self.client.index(index="argus-alerts",document=document)
        except Exception as e:
            print(f"[ES ERROR] {e}")

        return self.client.index(index="argus-alerts",document=document)

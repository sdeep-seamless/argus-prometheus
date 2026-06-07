from dotenv import load_dotenv
import os

load_dotenv()

ELASTIC_URL = os.getenv(
    "ELASTIC_URL",
    "http://state-machine:9200"
)

PROMETHEUS_URL = os.getenv(
    "PROMETHEUS_URL",
    "http://prometheus:9090"
)

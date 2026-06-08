from datetime import datetime

class AlertService:

    def create(
        self,
        anomaly
    ):

        return {
            "timestamp":
                datetime.now().isoformat(), 
            "instance":
                anomaly["instance"],
            "metric":
                anomaly["metric"],
            "type":
                anomaly["type"],
            "value":
                anomaly["value"],
            "z_score":
                anomaly["z_score"]
        }

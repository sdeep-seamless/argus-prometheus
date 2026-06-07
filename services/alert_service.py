from datetime import datetime

class AlertService:

    def create(
        self,
        anomaly
    ):

        return {
            "timestamp":
                datetime.utcnow(),
            "instance":
                anomaly["instance"],
            "type":
                anomaly["type"],
            "value":
                anomaly["value"],
            "z_score":
                anomaly["z_score"]
        }

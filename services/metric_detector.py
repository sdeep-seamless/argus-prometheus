class MetricDetector:

    def detect(
        self,
        metric_name,
        current_value,
        baseline,
    ):

        mean = baseline["mean"]
        std = baseline["std"]

        if std == 0:
            return None

        z_score = (
            current_value - mean
        ) / std

        print(
            f"[DETECTOR] "
            f"Current={current_value} "
            f"Mean={mean} "
            f"STD={std} "
            f"Z={z_score}"
        )

        if abs(z_score) > 3:

            return {
                "type":f"{metric_name}_anomaly",
                "metric": metric_name,
                "value": current_value,
                "z_score": z_score
            }

        return None

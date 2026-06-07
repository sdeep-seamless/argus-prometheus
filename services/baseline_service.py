import numpy as np

baseline_cache = {}

class BaselineService:

    def update(
        self,
        metric_name,
        instance,
        values
    ):

        if metric_name not in baseline_cache:
            baseline_cache[metric_name] = {}
        baseline_cache[metric_name][instance] = {"mean": float(np.mean(values)),"std": float(np.std(values))}

        print(
        f"[BASELINE] {metric_name}: "
        f"{baseline_cache[metric_name]}"
    )

    def get(
        self,
        metric_name,
        instance
    ):
        metric_data = baseline_cache.get(metric_name,{})
        return metric_data.get(instance)
#        return baseline_cache.get(
#            metric_name
#        )

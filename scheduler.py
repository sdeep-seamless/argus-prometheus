import schedule
import time
from datetime import datetime

#=============== 1. Baseline Collection Job ==================

from services.prometheus_service import (
    PrometheusService
)

from services.baseline_service import (
    BaselineService
)

from services.metric_detector import (
    MetricDetector
)

from services.alert_service import (
    AlertService
)

from services.elasticsearch_service import (
    ElasticsearchService
)

prom = PrometheusService()
baseline = BaselineService()
detector = MetricDetector()
alerts = AlertService()
es = ElasticsearchService()

cpu_history = {}
memory_history = {}
network_history = {}


def collect_cpu_baseline():

    results = prom.get_cpu_usage()

    if not results:
        print("[WARN] No CPU data returned from Prometheus.")
        return

    for item in results:

        instance = item["metric"]["instance"]

        value = float(
            item["value"][1]
        )

        if instance not in cpu_history:
            cpu_history[instance] = []

        cpu_history[instance].append(value)

        if len(cpu_history[instance]) > 1440:
            cpu_history[instance].pop(0)

        baseline.update(metric_name="cpu",instance=instance,values=cpu_history[instance])

        #baseline_data = baseline.get("cpu",instance)
        #es.save_metric({"@timestamp":datetime.now().isoformat(),"instance":instance,"metric":"cpu","value":value,"mean":baseline_data["mean"],"std":baseline_data["std"})



#cpu_history = []

#def collect_baseline():
#
#    result = (prom.get_cpu_usage())
##    print(f"PROMETHEUS RESULT = {result}")
#
#    if not result:
#        print("No CPU metrics returned from Prometheus")
#        return
#
#    value = float(result[0]["value"][1]) # Only uses first node for Test
#    cpu_history.append(value)
#
#    if len(cpu_history) > 1440:
#        cpu_history.pop(0)
#
#    baseline.update("cpu",cpu_history)
#
## During MVP run
##schedule.every(1).minutes.do(
##    collect_cpu_baseline
##)
#
# During Testing
schedule.every(10).seconds.do(
    collect_cpu_baseline
)

def collect_memory_baseline():

    results = prom.get_memory_usage()

    if not results:
        return

    for item in results:
        instance = (item["metric"]["instance"])
        value = float(item["value"][1])

        if instance not in memory_history:
            memory_history[instance] = []

        memory_history[instance].append(value)

        if len(memory_history[instance]) > 1440:
            memory_history[instance].pop(0)

        baseline.update(metric_name="memory",instance=instance,values=memory_history[instance])

        #baseline_data = baseline.get("memory",instance)
        #es.save_metric({"@timestamp":datetime.now().isoformat(),"instance":instance,"metric":"memory","value":value,"mean":baseline_data["mean"],"std":baseline_data["std"})



schedule.every(10).seconds.do(
    collect_memory_baseline
)



def collect_network_baseline():

    results = prom.get_network_usage()

    if not results:
        return

    for item in results:
        instance = (item["metric"]["instance"])
        value = float(item["value"][1])

        if instance not in network_history:
            network_history[instance] = []

        network_history[instance].append(value)

        if len(network_history[instance]) > 1440:
            network_history[instance].pop(0)

        baseline.update(metric_name="network",instance=instance,values=network_history[instance])

        #baseline_data = baseline.get("network",instance)
        #es.save_metric({"@timestamp":datetime.now().isoformat(),"instance":instance,"metric":"network","value":value,"mean":baseline_data["mean"],"std":baseline_data["std"})



schedule.every(10).seconds.do(
    collect_network_baseline
)

#============= 2. Detection Job ===============



def detect_cpu():

    results = prom.get_cpu_usage()

    if not results:
        return

    for item in results:
        instance = (item["metric"]["instance"])
        current = float(item["value"][1])
        baseline_data = (baseline.get("cpu",instance))

        if not baseline_data:
            continue

        print(
        f"[CHECKING] "
        f"{instance} "
        f"CPU={current}"
        )


        anomaly = detector.detect("cpu",current,baseline_data) # type, metric, value, z_score

        if anomaly:
            anomaly["instance"] = (instance)
            alert = alerts.create(anomaly)
            #es.save_alert(alert)
            es.save_metric({"@timestamp":datetime.now().isoformat(),"instance":instance,"metric":"cpu","value":"{current}","type":"cpu_anomaly","mean":baseline_data["mean"],"std":baseline_data["std"],"z_score":anomaly["z_score"]})
            es.save_alert({"@timestamp":datetime.now().isoformat(),"instance":instance,"metric":"cpu","value":"{current}","type":"cpu_anomaly","mean":baseline_data["mean"],"std":baseline_data["std"],"z_score":anomaly["z_score"]})
            print("\n========== ALERT ==========")
            print(alert)
            print("===========================\n")
        else:
            es.save_metric({"@timestamp":datetime.now().isoformat(),"instance":instance,"metric":"cpu","value":"{current}","type":"cpu_anomaly","mean":baseline_data["mean"],"std":baseline_data["std"],"z_score":"normal"})



#def detect_cpu():
#
#    if len(cpu_history) < 10:
#        print("[INFO] Waiting for baseline")
#        return
#
#    current = float(prom.get_cpu_usage()[0]["value"][1])
#    baseline_data = (baseline.get("cpu"))
#
#    if not baseline_data:
#        print("[INFO] Baseline not ready")
#        return
#
#    anomaly = detector.detect(current,baseline_data)
#
#    if anomaly:
#        alert = alerts.create(anomaly)
#        print("\n========== ALERT ==========")
#        print(alert)
#        print("===========================\n")
#

# During MVP
#schedule.every(5).minutes.do(
#    detect_cpu
#)

# During Test
schedule.every(20).seconds.do(
    detect_cpu
)

def detect_memory():

    results = prom.get_memory_usage()

    if not results:
        return

    for item in results:

        instance = (item["metric"]["instance"])
        current = float(item["value"][1])
        baseline_data = baseline.get("memory",instance)

        if not baseline_data:
            continue
        print(
        f"[CHECKING] "
        f"{instance} "
        f"RAM={current}"
        )

        anomaly = detector.detect("memory",current,baseline_data)

        if anomaly:
            anomaly["instance"] = (instance)
            alert = alerts.create(anomaly)
            es.save_metric({"@timestamp":datetime.now().isoformat(),"instance":instance,"metric":"memory","value":"{current}","type":"memory_anomaly","mean":baseline_data["mean"],"std":baseline_data["std"],"z_score":anomaly["z_score"]})
            es.save_alert({"@timestamp":datetime.now().isoformat(),"instance":instance,"metric":"memory","value":"{current}","type":"memory_anomaly","mean":baseline_data["mean"],"std":baseline_data["std"],"z_score":anomaly["z_score"]})
            #es.save_alert(alert)
            print("\n========== ALERT ==========")
            print(alert)
            print("===========================\n")
        else:
            es.save_metric({"@timestamp":datetime.now().isoformat(),"instance":instance,"metric":"memory","value":"{current}","type":"memory_anomaly","mean":baseline_data["mean"],"std":baseline_data["std"],"z_score":"normal"]})

schedule.every(20).seconds.do(
    detect_memory
)


def detect_network():

    results = prom.get_network_usage()

    if not results:
        return

    for item in results:
        instance = (item["metric"]["instance"])
        current = float(item["value"][1])
        baseline_data = baseline.get("network",instance)

        if not baseline_data:
            continue
        print(
        f"[CHECKING] "
        f"{instance} "
        f"NETWORK={current}"
        )

        anomaly = detector.detect("network",current,baseline_data)

        if anomaly:
            anomaly["instance"] = (instance)
            alert = alerts.create(anomaly)
            es.save_metric({"@timestamp":datetime.now().isoformat(),"instance":instance,"metric":"network","value":"{current}","type":"network_anomaly","mean":baseline_data["mean"],"std":baseline_data["std"],"z_score":anomaly["z_score"]})
            es.save_alert({"@timestamp":datetime.now().isoformat(),"instance":instance,"metric":"network","value":"{current}","type":"network_anomaly","mean":baseline_data["mean"],"std":baseline_data["std"],"z_score":anomaly["z_score"]})
            #es.save_alert(alert)
            print("\n========== ALERT ==========")
            print(alert)
            print("===========================\n")
        else:
            es.save_metric({"@timestamp":datetime.now().isoformat(),"instance":instance,"metric":"network","value":"{current}","type":"network_anomaly","mean":baseline_data["mean"],"std":baseline_data["std"],"z_score":"normal"]})

schedule.every(20).seconds.do(
    detect_network
)


# Call scope



while True:
    schedule.run_pending()
    time.sleep(1)


import time
import threading
import requests
from datetime import datetime

def start_health_check(message_handler, services, sleep_amount, anomaly_threshold):
    thread = threading.Thread(target=check, args=(message_handler, services, sleep_amount, anomaly_threshold))
    thread.start()

def check(message_handler, services, sleep_amount, anomaly_threshold):
    error_status = {name: False for name in services}
    anomalies = {name: 0 for name in services}

    while True:
        for service_name, service_url in services.items():
            check_status(service_name, service_url, anomalies, error_status, message_handler, anomaly_threshold)
        time.sleep(sleep_amount)

def check_status(service_name, service_url, anomalies, error_status, message_handler, anomaly_threshold):
    response = requests.get(url=service_url)

    if not is_ok(response):
        print(f'[{datetime.now().isoformat()}] {service_name} returned {response.status_code}')

    is_in_error = error_status[service_name]

    if is_in_error ^ is_ok(response):
        anomalies[service_name] = 0
        return

    anomalies[service_name] += 1

    if not should_alarm(service_name, anomalies, anomaly_threshold):
        return

    if is_in_error:
        message = f'{service_name} is OK, all issues resolved.'
    else:
        message = f'{service_name} is down, received {response.status_code} trying to access {service_url}'

    considered = 'UP' if is_in_error else 'DOWN'
    print(f'[{datetime.now().isoformat()}] {service_name} was considered {considered}')


    message_handler.broadcast(message, service_name)
    error_status[service_name] = not error_status[service_name]
    anomalies[service_name] = 0

def should_alarm(service_name, anomalies, anomaly_threshold):
    return anomalies[service_name] >= anomaly_threshold

def is_ok(response):
    return 200 <= response.status_code < 300
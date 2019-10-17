import time
import threading
import requests


def start_health_check(telegram_handler, services, sleep_amount, anomaly_threshold):
    thread = threading.Thread(target=check, args=(telegram_handler, services, sleep_amount, anomaly_threshold))
    thread.start()

def check(telegram_handler, services, sleep_amount, anomaly_threshold):
    error_status = {name: False for name in services}
    anomalies = {name: 0 for name in services}

    while True:
        for service_name, service_url in services.items():
            check_status(service_name, service_url, anomalies, error_status, telegram_handler, anomaly_threshold)
        time.sleep(sleep_amount)

def check_status(service_name, service_url, anomalies, error_status, telegram_handler, anomaly_threshold):
    response = requests.get(url=service_url)
    print(f'{service_name} returned {response.status_code}')
    is_in_error = error_status[service_name]
    
    if is_in_error ^ is_ok(response):
        anomalies[service_name] = 0
        return

    anomalies[service_name] += 1
    if should_alarm(service_name, anomalies, anomaly_threshold):
        message_type = 'ok' if is_in_error else 'not ok'

        print({'name': service_name, 'message_type': message_type, 'anomalies': anomalies})

        if message_type == 'not ok':
            message = f'{service_name} is down, received {response.status_code} trying to access {service_url}'
            telegram_handler.broadcast(message)
            error_status[service_name] = True
            anomalies[service_name] = 0
        
        else:
            message = f'{service_name} is OK, all issues resolved.'
            telegram_handler.broadcast(message)
            error_status[service_name] = False
            anomalies[service_name] = 0

def should_alarm(service_name, anomalies, anomaly_threshold):
    return anomalies[service_name] >= anomaly_threshold

def is_ok(response):
    return str(response.status_code).startswith('2')
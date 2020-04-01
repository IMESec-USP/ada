import time
import threading
import requests
from datetime import datetime
from abc import ABC, abstractmethod


class EventHandler(ABC):
    @abstractmethod
    def broadcast(self, message, service_name, status):
        pass


class TelegramEventHandler(EventHandler):

    def __init__(self, telegram_handler):
        self.telegram_handler = telegram_handler

    def broadcast(self, message, service_name, status):
        self.telegram_handler.broadcast(message, service_name)


def start_health_check(event_handler, services, sleep_amount, anomaly_threshold):

    message_handler = event_handler if isinstance(event_handler, EventHandler) else TelegramEventHandler(event_handler)
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
    response = None
    exception = None
    try:
        response = requests.get(url=service_url)
    except requests.exceptions.RequestException as e:
        exception = e

    if not is_ok(response):
        print(f'[{datetime.now().isoformat()}] {service_name} returned {response.status_code if response is not None else exception}')

    is_in_error = error_status[service_name]

    if is_in_error ^ is_ok(response):
        anomalies[service_name] = 0
        return

    anomalies[service_name] += 1

    if not should_alarm(service_name, anomalies, anomaly_threshold):
        return

    if is_in_error:
        message = f'{service_name} is OK, all issues resolved.'
    elif response is None:
        message = f'{service_name} is down, received the exception {exception} when trying to access {service_url}'
    else:
        message = f'{service_name} is down, received {response.status_code} trying to access {service_url}'

    considered = 'UP' if is_in_error else 'DOWN'
    print(f'[{datetime.now().isoformat()}] {service_name} was considered {considered}')

    message_handler.broadcast(message, service_name, considered)
    error_status[service_name] = not error_status[service_name]
    anomalies[service_name] = 0


def should_alarm(service_name, anomalies, anomaly_threshold):
    return anomalies[service_name] >= anomaly_threshold


def is_ok(response):
    return response is not None and 200 <= response.status_code < 300

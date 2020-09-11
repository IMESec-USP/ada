#!/usr/bin/env python3
from healthcheck.health_check import start_health_check, EventHandler, HealthStatus
from utils.logger import Logger
from utils.telegram import TelegramHandler

from constants import (STICKER_ID_KK_MORRI, TELEGRAM_API_TOKEN,
                       CONVERSATIONS,
                       ADA_URL,
                       HEALTHCHECK_SLEEP_AMOUNT,
                       HEALTHCHECK_ANOMALY_THRESHOLD)


class BackupHandler(EventHandler):
    def __init__(self, telegram_handler):
        self.telegram_handler = telegram_handler

    def broadcast(self, message, service_name, status):
        # we only care about ada right now
        if service_name != 'Ada': return
        if status == HealthStatus.UP:
            print("It's a miracle! Ada is back to life")
            self.telegram_handler.broadcast('Meu serviço principal foi restaurado. Estou de volta!')
        else:
            print('Ada is ded. Sending telegram message...')
            self.telegram_handler.broadcast(f"I don't feel so good... estou rodando como backup", sticker=STICKER_ID_KK_MORRI)


if __name__ == '__main__':
    logger = Logger(None)
    handler = TelegramHandler(logger, TELEGRAM_API_TOKEN, CONVERSATIONS)
    backup_handler = BackupHandler(handler)
    start_health_check(logger, backup_handler, {'Ada': ADA_URL}, HEALTHCHECK_SLEEP_AMOUNT, HEALTHCHECK_ANOMALY_THRESHOLD)


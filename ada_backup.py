
from func_timeout import StoppableThread

from healthcheck.health_check import start_health_check, EventHandler
from utils.logger import Logger
from utils.telegram import TelegramHandler

from constants import (TELEGRAM_API_TOKEN,
                       CONVERSATIONS,
                       ADA_URL,
                       HEALTHCHECK_SERVICES,
                       HEALTHCHECK_SLEEP_AMOUNT,
                       HEALTHCHECK_ANOMALY_THRESHOLD)


class BackupHandler(EventHandler):
    def __init__(self, telegram_handler):
        self.telegram_handler = telegram_handler

    def broadcast(self, message, service_name, status):
        # we only care about ada right now
        if service_name != "Ada": return
        if status == "UP":
            print("It's a miracle! Ada is back to life")
            self.telegram_handler.broadcast("Meu serviço principal foi restaurado. Estou de volta!")
        else:
            print("ada is ded. starting healthcheck thread")
            self.telegram_handler.broadcast(f"I don't feel so good... Acho que eu morri, estou rodando como backup")


if __name__ == "__main__":
    logger = Logger(None)
    handler = TelegramHandler(TELEGRAM_API_TOKEN, CONVERSATIONS)
    backup_handler = BackupHandler(handler)
    start_health_check(backup_handler, {"Ada": ADA_URL}, HEALTHCHECK_SLEEP_AMOUNT, HEALTHCHECK_ANOMALY_THRESHOLD)


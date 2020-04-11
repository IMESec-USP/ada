import falcon

from middleware.github_signature import GithubSignatureVerifier
from middleware.json_loader import JsonLoader
from middleware.logger import LoggerMiddleware

from resources.github import Github
from resources.docker_hub import DockerHub
from resources.self_health import SelfHealth

from utils.logger import Logger
from utils.telegram import TelegramHandler

from healthcheck.health_check import start_health_check, TelegramEventHandler

from constants import (TELEGRAM_API_TOKEN,
                       CONVERSATIONS,
                       GITHUB_SECRET,
                       HEALTHCHECK_SERVICES,
                       HEALTHCHECK_SLEEP_AMOUNT,
                       HEALTHCHECK_ANOMALY_THRESHOLD)


def create():
    logger = Logger(None)
    telegram_handler = TelegramHandler(logger, TELEGRAM_API_TOKEN, CONVERSATIONS)
    telegram_handler.poll()

    api = falcon.API(middleware=[
        LoggerMiddleware(logger),
        GithubSignatureVerifier(logger, GITHUB_SECRET),
        JsonLoader(logger),
    ])

    github_resource = Github(logger, telegram_handler)
    dockerhub_resource = DockerHub(logger, telegram_handler)
    selfhealth_resource = SelfHealth(logger, telegram_handler)

    api.add_route('/github', github_resource)
    api.add_route('/dockerhub', dockerhub_resource)
    api.add_route('/_healthcheck', selfhealth_resource)
    start_health_check(TelegramEventHandler(telegram_handler), HEALTHCHECK_SERVICES, HEALTHCHECK_SLEEP_AMOUNT, HEALTHCHECK_ANOMALY_THRESHOLD)
    return api


app = application = create()

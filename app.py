import falcon

from middleware.github_signature import GithubSignatureVerifier
from middleware.json_loader import JsonLoader
from middleware.logger import LoggerMiddleware

from resources.github import Github
from resources.docker_hub import DockerHub
from resources.metastatus import Metastatus

from utils.logger import Logger
from utils.telegram import TelegramHandler

from healthcheck.health_check import start_health_check

from constants import (TELEGRAM_API_TOKEN,
                       CONVERSATIONS,
                       GITHUB_SECRET,
                       HEALTHCHECK_SERVICES,
                       HEALTHCHECK_SLEEP_AMOUNT,
                       HEALTHCHECK_ANOMALY_THRESHOLD)


def create():
    logger = Logger(None)
    handler = TelegramHandler(TELEGRAM_API_TOKEN, CONVERSATIONS)
    handler.poll()

    api = falcon.API(middleware=[
        LoggerMiddleware(logger),
        GithubSignatureVerifier(GITHUB_SECRET),
        JsonLoader(),
    ])

    print('polling Telegram...')

    github_resource = Github(logger, handler)
    dockerhub_resource = DockerHub(logger, handler)
    metastatus_resource = Metastatus(logger, handler)

    api.add_route('/github', github_resource)
    api.add_route('/dockerhub', dockerhub_resource)
    api.add_route('/_healthcheck', metastatus_resource)
    start_health_check(handler, HEALTHCHECK_SERVICES, HEALTHCHECK_SLEEP_AMOUNT, HEALTHCHECK_ANOMALY_THRESHOLD)
    return api


app = application = create()


from .base import BaseResource
import requests

class DockerHub(BaseResource):

    def __init__(self, logger, telegram_broadcaster):
        super().__init__(logger, telegram_broadcaster)

    def on_post(self, req, res):
        body = req.context.body
        repo_name = body['repository']['repo_name']
        tag = body['push_data']['tag']
        pusher = body['push_data']['pusher']

        message = '\n'.join([
            f'Nova imagem de docker no repositório {repo_name}:{tag},',
            f'criada por {pusher}',
        ])
        self.broadcaster.broadcast(message, 'imesec-core')

        self.activate_callback(body)

    def activate_callback(self, body):
        callback_url = body['callback_url']
        requests.post(callback_url, json={
            'state': 'success',
        })
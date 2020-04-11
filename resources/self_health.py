import falcon
import json

from .base import BaseResource


class SelfHealth(BaseResource):

    def __init__(self, logger, telegram_broadcaster):
        super().__init__(logger, telegram_broadcaster)
        self.has_json_body = False
        self.ignore_middleware_log = True

    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        res.body = json.dumps({
                'msg': 'pong.'
            }).encode('utf-8')
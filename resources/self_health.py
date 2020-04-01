import falcon
import json

from .base import BaseResource


class SelfHealth(BaseResource):

    def on_get(self, req, res):
        
        res.status = falcon.HTTP_200
        res.body = json.dumps({
                'msg': 'pong.'
            }).encode('utf-8')
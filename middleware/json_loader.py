import json
import falcon


class JsonLoader:

    def __init__(self, ignored_routes=None):
        self.ignored_routes = ignored_routes if ignored_routes is not None else []

    def process_resource(self, req, res, resource, params):
        # dont parse json if we just want the status
        if resource.__class__.__name__ in self.ignored_routes:
            return
        try:
            req.context.body = json.loads(req.context.body)
        except json.decoder.JSONDecodeError:
            res.status = falcon.HTTP_400
            res.body = json.dumps({
                'error': 'Expected JSON in body.'
            }).encode('utf-8')
            res.complete = True

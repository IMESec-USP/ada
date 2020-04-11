import json
import falcon


class JsonLoader:
    def __init__(self, logger):
        self.logger = logger.with_class_name(self)

    def process_resource(self, req, res, resource, params):
        if not resource.has_json_body:
            return
        try:
            req.context.body = json.loads(req.context.body)
        except json.decoder.JSONDecodeError:
            self.logger.log(f'Could not decode JSON body of request to {resource.__class__.__name__}')
            res.status = falcon.HTTP_400
            res.body = json.dumps({
                'error': 'Expected JSON in body.'
            }).encode('utf-8')
            res.complete = True

import json
import falcon


class JsonLoader:

    def process_resource(self, req, res, resource, params):
        if not resource.has_json_body:
            return
        try:
            req.context.body = json.loads(req.context.body)
        except json.decoder.JSONDecodeError:
            res.status = falcon.HTTP_400
            res.body = json.dumps({
                'error': 'Expected JSON in body.'
            }).encode('utf-8')
            res.complete = True

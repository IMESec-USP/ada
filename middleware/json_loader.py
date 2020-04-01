import json
import falcon


class JsonLoader:

    def process_resource(self, req, res, resource, params):
        # dont parse json if we just want the status
        if type(resource).__name__ == "Metastatus":
            return
        try:
            req.context.body = json.loads(req.context.body)
        except json.decoder.JSONDecodeError:
            res.status = falcon.HTTP_400
            res.body = json.dumps({
                'error': 'Expected JSON in body.'
            }).encode('utf-8')
            res.complete = True

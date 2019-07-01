class LoggerMiddleware:

    def __init__(self, logger):
        self.logger = logger

    def process_response(self, req, res, resource, req_succeded):
        self.logger.log(f'{res.status} {req.method} {req.relative_uri}')
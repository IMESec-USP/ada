class LoggerMiddleware:

    def __init__(self, logger):
        self.logger = logger.with_class_name(self)

    def process_response(self, req, res, resource, req_succeded):
        if getattr(resource, 'ignore_middleware_log', False):
            return
        self.logger.log(f'{res.status} {req.method} {req.relative_uri}')
from hashlib import sha1
import hmac
import falcon
import json

from resources.github import Github

class GithubSignatureVerifier:

    def __init__(self, logger, github_secret):
        self.github_secret = bytes(github_secret, 'utf-8')
        self.logger = logger.with_class_name(self)

    def process_resource(self, req, res, resource, params):
        body_bytes = req.bounded_stream.read()
        req.context.body = body_bytes

        if not isinstance(resource, Github):
            return

        signature = req.get_header('X-Hub-Signature')
        body_hash = hmac.new(self.github_secret, body_bytes, sha1)
        digest = 'sha1=' + body_hash.hexdigest()

        if signature is None or not hmac.compare_digest(digest, signature):
            self.logger.log('Received invalid signature for a github request')
            res.status = falcon.HTTP_400
            res.body = json.dumps({
                'error': 'Could not verify request signature'
            }).encode('utf-8')
            res.complete = True
import falcon
import json

from .base import BaseResource


class Github(BaseResource):

    def __init__(self, logger, telegram_broadcaster):
        super().__init__(logger, telegram_broadcaster)
        self.handle_functions = {
            'pull_request': self.handle_pull_request,
            'issues': self.handle_issue,
        }
        self.has_json_body = True
        self.ignore_middleware_log = False

    def on_post(self, req, res):
        body = req.context.body
        action = req.get_header('X-GitHub-Event')
        handler = self.handle_functions.get(action)

        self.logger.log(f'handling action "{action}"')
        if handler is not None:
            handler(body)

        res.status = falcon.HTTP_200

    def handle_issue(self, body: dict):
        action = body['action']
        if action not in ['opened', 'closed', 'reopened']:
            return

        title = body['issue']['title']
        creator = body['issue']['user']['login']
        url = body['issue']['html_url']
        message_verb = 'fechou' if action == 'closed' else 'abriu'
        message = '\n'.join([
            f'{creator} {message_verb} uma issue: {title}',
            url,
        ])

        self.logger.log(f'broadcasting message about issue {action}')
        self.broadcaster.broadcast(message, 'issue')

    def handle_pull_request(self, body: dict):
        target_branch = body['pull_request']['base']['ref']
        if target_branch != 'master':
            return

        action = body['action']
        if action not in ['opened', 'closed']:
            return

        repository_name = body['repository']['full_name']
        title = body['pull_request']['title']
        sender = body['sender']['login']

        url = body['pull_request']['html_url']
        message_verb = 'abriu' if action == 'opened' else 'fechou'
        message = '\n'.join([
            f'{sender} {message_verb} um pull request:',
            f'{title}',
            f'Link: {url}'
        ])
        self.logger.log(f'broadcasting pull request on {repository_name}')
        self.broadcaster.broadcast(message, repository_name)
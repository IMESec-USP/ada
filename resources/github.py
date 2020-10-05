import falcon
import json

from .base import BaseResource


class Github(BaseResource):

    verbs = {
        'opened': 'abriu',
        'locked': 'trancou',
        'unlocked': 'destrancou',
        'deleted': 'deletou',
        'reopened': 'reabriu',
        'closed': 'fechou',
        'review_requested': 'pediu review em',
    }

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
        title = body['issue']['title']
        creator = body['issue']['user']['login']
        number = body['issue']['number']
        url = body['issue']['html_url']

        if not action in self.verbs:
            self.logger.log(f'Unsupported action received: {action}')
            return
        message_verb = self.verbs[action]

        message = f'{creator} {message_verb} uma issue: [\#{number} \- `{title}`]({url})'

        self.logger.log(f'broadcasting message about issue {action}')
        self.broadcaster.broadcast(message, 'issue', parse_mode='MarkdownV2')

    def handle_pull_request(self, body: dict):
        target_branch = body['pull_request']['base']['ref']
        if target_branch not in ['master', 'main']:
            return

        action = body['action']
        repository_name = body['repository']['full_name']
        title = body['pull_request']['title']
        number = body['number']
        sender = body['sender']['login']
        merged = body['pull_request']['merged']
        url = body['pull_request']['html_url']

        if not action in self.verbs:
            self.logger.log(f'Unsupported action received: {action}')
            return
        message_verb = self.verbs[action]

        if action == 'closed' and merged:
            message_verb = 'mergeou'
        
        message = '\n'.join([
            f'{sender} {message_verb} um pull request:',
            f'[\#{number} \- `{title}`]({url})'
        ])
        self.logger.log(f'broadcasting pull request on {repository_name}')
        self.broadcaster.broadcast(message, repository_name, parse_mode='MarkdownV2')
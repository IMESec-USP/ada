import falcon
import json

from .base import BaseResource


class Github(BaseResource):

    def __init__(self, logger, telegram_broadcaster):
        super().__init__(logger, telegram_broadcaster)
        self.handle_functions = {
            'push': self.handle_commit,
            'pull_request': self.handle_pull_request,
        }
        self.has_json_body = True
        self.ignore_middleware_log = False

    def on_post(self, req, res):
        body = req.context.body
        action = req.get_header('X-GitHub-Event')
        handler = self.handle_functions.get(action)

        if handler is not None:
            handler(body)

        res.status = falcon.HTTP_200

    def handle_commit(self, body: dict):
        if 'master' not in body['ref']:
            return

        branch_name = body['ref']
        commits = body['commits']
        compare_link = body['compare']
        repository_name = body['repository']['full_name']
        pusher = body['pusher']['name']
        plural = 's' if len(commits) != 1 else ''
        message = '\n'.join([
            f'{pusher} Adicionou {len(commits)} commit{plural} a {repository_name}:{branch_name}.',
            f'Link para comparação: {compare_link}'
        ])
        self.broadcaster.broadcast(message, repository_name)

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
        self.broadcaster.broadcast(message, repository_name)
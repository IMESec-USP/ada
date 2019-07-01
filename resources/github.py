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

        branch_name = body['ref'].split('/')[-1]
        commits = body['commits']
        compare_link = body['compare']
        repository_name = body['repository']['full_name']
        commit_messages = ['- ' + commit['message'] for commit in commits]
        pusher = body['pusher']['name']
        plural = 's' if len(commit_messages) != 1 else ''
        message = '\n'.join([
            f'{pusher} Adicionou {len(commit_messages)} commit{plural} a {repository_name}:{branch_name}.',
            *commit_messages,
            '',
            f'Link para comparação: {compare_link}'
        ])
        self.broadcaster.broadcast(message)

    def handle_pull_request(self, body: dict):
        target_branch = body['pull_request']['base']['ref']
        if target_branch != 'master':
            return

        incoming_branch = body['pull_request']['head']['ref']
        title = body['pull_request']['title']
        sender = body['sender']['login']
        action = body['action']
        url = body['pull_request']['html_url']
        message = '\n'.join([
            'Novo status em um pull request:',
            f'Usuário: {sender}',
            f'Ação: {action}',
            f'Título: {title}',
            f'Branch alvo: {target_branch}',
            f'Branch sendo mergeada: {incoming_branch}',
            f'Link: {url}'
        ])
        self.broadcaster.broadcast(message)
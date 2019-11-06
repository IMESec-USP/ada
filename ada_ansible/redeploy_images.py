from .execute import execute

def redeploy_images() -> list:
    # This is the play that will be executed.
    playbook =  dict(
        name = 'Redeploy images in IMEsec swarm managers',
        hosts = 'swarm_managers',
        gather_facts = 'yes',
        tasks = [
            dict(action=dict(module='shell', args='docker stack deploy imesec -c /services/imesec-stack.yml'), register='shell_out'),
        ]
    )
    return execute(playbook)

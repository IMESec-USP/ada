from .execute import execute

def redeploy_images() -> list:
    # This is the play that will be executed.
    playbook =  dict(
        name = 'Redeploy images in IMEsec swarm managers',
        hosts = 'swarm_managers',
        gather_facts = 'yes',
        tasks = [
            dict(action=dict(module='shell', args='ls'), register='shell_out'),
            dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
        ]
    )
    return execute(playbook)
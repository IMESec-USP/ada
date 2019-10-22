import shutil

from ansible import context
from ansible.cli import CLI
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.inventory.manager import InventoryManager
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.vars.manager import VariableManager
import ansible.constants as C

from .global_ansible_lock import GlobalLock
from .lock_exception import AnsibleLockException

def execute(playbook: dict) -> list:
    ''' executes an arbitrary playbook '''

    try:
        with GlobalLock:
            # Since ansible has shit documentation, i'll use comments
            # to document for once.

            # this loader is the interpreter for all the yaml files.
            loader = DataLoader()

            # This is all the environment of the underlying ansible process
            context.CLIARGS = ImmutableDict(tags={}, listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh',
                                module_path=None, forks=100, remote_user='razgrizone', private_key_file='~/.ssh/imesec',
                                ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True,
                                become_method='sudo', become_user='root', verbosity=True, check=False, start_at_task=None)

            # Here, we load the ansible hosts file.
            inventory = InventoryManager(loader=loader, sources='ada_ansible/ansible-playbooks/hosts')
            passwords = {}

            # We merge the variables from CLI.
            # variable manager takes care of merging all the different sources to give you a unified view of variables available in each context
            variable_manager = VariableManager(loader=loader, inventory=inventory, version_info=CLI.version_info(gitinfo=False))

            # We create a play based on the playbook, 
            # creating the task objects from the info provided
            play = Play().load(playbook, variable_manager=variable_manager, loader=loader)
            
            # Run it - instantiate task queue manager, which takes care of forking and setting up all objects to iterate over host list and tasks
            tqm = None
            try:
                tqm = TaskQueueManager(
                        inventory=inventory,
                        variable_manager=variable_manager,
                        loader=loader,
                        passwords=passwords,
                        # stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
                    )
                return tqm.run(play) # most interesting data for a play is actually sent to the callback's methods
            finally:
                # we always need to cleanup child procs and the structures we use to communicate with them
                if tqm is not None:
                    tqm.cleanup()

                # Remove ansible tmpdir
                shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)


    except AnsibleLockException:
        return None

from colab_ssh._command import run_command as _run_command
import os

def init_git(repositoryUrl, branch="master"):
    _run_command("git clone {}".format(repositoryUrl))
    _run_command("git checkout {}".format(branch))

    # TODO: Create the folder if it doesn't exist
    os.system('mkdir -p ~/.ssh && curl -L -f {}/raw/{}/.colab_ssh/authorized_keys >> ~/.ssh/authorized_keys'.format(repositoryUrl.rstrip(".git"), branch))

    print("Successfully cloned the repository")
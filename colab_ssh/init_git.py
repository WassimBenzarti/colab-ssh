from colab_ssh._command import run_command as _run_command
import os

def init_git(repositoryUrl, branch="master"):
    _run_command("git clone {}".format(repositoryUrl))
    _run_command("git checkout {}".format(branch))

    os.system('curl -f {}/.colab_ssh/authorized_keys >> ~/.ssh/authorized_keys'.format(repositoryUrl.rstrip(".git")))

    print("Successfully cloned the repository")
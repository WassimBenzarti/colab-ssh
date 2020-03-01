from colab_ssh._command import run_command as _run_command

def init_git(repositoryUrl, branch="master"):
    _run_command("git clone {}".format(repositoryUrl))
    _run_command("git checkout {}".format(branch))
    print("Successfully cloned the repository")
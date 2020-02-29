from colab_ssh import run_command as _run_command

def init_git(repositoryUrl, branch):
    _run_command("git clone $repositoryUrl .")
    if branch: 
        _run_command("git checkout {}".format(branch))

    print("Successfully cloned the repository")
from colab_ssh._command import run_command as _run_command
import os

def init_git(repositoryUrl, branch="master", github_personal_token=""):
    _run_command("git clone {}".format(repositoryUrl))
    _run_command("git checkout {}".format(branch))

    # TODO: Create the folder if it doesn't exist
    os.system("mkdir -p ~/.ssh && curl -L -f {} {}/{}/.colab_ssh/authorized_keys >> ~/.ssh/authorized_keys".format(
        ("-H 'Authorization: token "+github_personal_token) if github_personal_token else "",
        repositoryUrl.rstrip(".git").replace("github.com", "raw.githubusercontent.com"), 
        branch))

    print("Successfully cloned the repository")
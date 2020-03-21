from colab_ssh._command import run_command as _run_command
import os
import sys


def parse_folder_name(array):
    import re
    sys.path.insert(0, "./"+re.search("'(.*?)'", array[0]).groups(1)[0])

def init_git(repositoryUrl, 
            branch="master", 
            personal_token="", 
            email=None, 
            username=None):
    # Clone the repository then add the folder to the sys.path
    _run_command("git clone {}".format(
            repositoryUrl.replace("github.com", personal_token+"@github.com")if personal_token else repositoryUrl) ,
            callback=parse_folder_name
    )

    # Checkout the branch
    os.system('cd "$(basename {} .git)" && git checkout {}'.format(repositoryUrl,branch))

    # Add the email and username
    if email: os.system('git config --global user.email "{}"'.format(email))
    if username: os.system('git config --global user.name "{}"'.format(username))
    

    os.system("mkdir -p ~/.ssh && curl -L -f {} {}/{}/.colab_ssh/authorized_keys >> ~/.ssh/authorized_keys".format(
        ("-H 'Authorization: token {}'".format(personal_token)) if personal_token else "",
        repositoryUrl.split(".git")[0].replace("github.com", "raw.githubusercontent.com"), 
        branch))

    print("Successfully cloned the repository")

    

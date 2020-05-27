from colab_ssh._command import run_command as _run_command
import os
import sys
import importlib
import requests
from .get_tunnel_config import get_tunnel_config


def parse_folder_name(array):
    import re
    sys.path.insert(0, "./"+re.search("'(.*?)'", array[0]).groups(1)[0])

def init_git(repositoryUrl, 
            branch="master", 
            personal_token="", 
            email=None, 
            username=None,
            verbose=False):
    # Clone the repository then add the folder to the sys.path
    _run_command("git clone {}".format(
            repositoryUrl.replace("github.com", personal_token+"@github.com")if personal_token else repositoryUrl) ,
            callback=parse_folder_name
    )

    repo_name = os.path.basename(repositoryUrl).rstrip(".git") 

    # Checkout the branch
    os.system(f'cd {repo_name} && git checkout {branch}')
    
    # Make sure that even if the repository is public, the personal token is still in the origin remote url
    if personal_token:
      os.system("git remote set-url origin {}".format(
        repositoryUrl.replace("github.com", personal_token+"@github.com")
      ))

    # Add the email and username
    if email: os.system('git config --global user.email "{}"'.format(email))
    if username: os.system('git config --global user.name "{}"'.format(username))
    
    # Bring the public key from the repository and paste it in the authorized_keys
    os.system("mkdir -p ~/.ssh && curl -s -L -f {} {}/{}/.colab_ssh/authorized_keys >> ~/.ssh/authorized_keys".format(
        ("-H 'Authorization: token {}'".format(personal_token)) if personal_token else "",
        repositoryUrl.split(".git")[0].replace("github.com", "raw.githubusercontent.com"), 
        branch))

    print('''Successfully cloned the repository''')

    # Print the VSCode direct link
    try:
      output = get_tunnel_config()
      link = f"vscode://vscode-remote/ssh-remote+root@{output['domain']}:{output['port']}/content/{repo_name}"
      if importlib.util.find_spec("IPython") and 'ipykernel' in sys.modules:
        from IPython.display import HTML, display
        display(
          HTML(
            f"""[Optional] You can open the cloned folder using VSCode, by clicking 
<a href='{link}'>{repo_name}</a>
            """
          )
        )
      else:
        print(f"[Optional] You can open the cloned folder using VSCode, by going to this url:\n{link}")
    except Exception as e:
      if verbose:
        print(e)

import logging
from colab_ssh._command import run_command as _run_command
import os
import sys
import importlib
import requests
from .get_tunnel_config import get_tunnel_config
import re
from urllib.parse import quote
from .utils import show_hint_message
from colab_ssh.utils.logger import get_logger

logger= get_logger()

def add_folder_to_sys_path(folder_path):
  sys.path.insert(0, folder_path)



def parse_cloning_output(array):
  git_logger= get_logger("git")
  # Successfully cloned
  if len(array) == 1:
      folder_path = "./"+re.search("'(.*?)'", array[0]).groups(1)[0]
      print('''Successfully cloned the repository in {}'''.format(folder_path))
      return add_folder_to_sys_path(folder_path)

  # Error occured in the cloning
  git_logger.debug(array)
  info, error, *rest = array
  git_logger.error(error)
  show_hint_message(error)


def init_git(repositoryUrl,
            branch="",
            personal_token="",
            email=None,
            username=None,
            verbose=False):
  # Add the Personal access token if available
  full_url = repositoryUrl.replace("github.com", personal_token+"@github.com") if personal_token else repositoryUrl
  
  if not personal_token:
    response = requests.get(full_url)
    if response.status_code == 200:
      logger.info("✔️ Public repository")
    else:
      # Get username if not passed
      username_input= input("Enter your username: (leave it empty if it's '{}')\n".format(username))
      username = quote(username_input or username)
      # Get password
      from getpass import getpass
      password = quote(getpass('Enter your password: \n'))
      if password:
        full_url = repositoryUrl.replace("github.com", "{}:{}@github.com".format(username, password))

  # Clone the repository then add the folder to the sys.path
  _run_command(
      "git clone {} {}".format(
        # Branch argument
        "--branch {}".format(branch) if branch else "",
        # Url argument
        full_url),
      callback=parse_cloning_output
  )

  repo_name = os.path.basename(repositoryUrl)
  repo_name, _ = os.path.splitext(repo_name)

  # Checkout the branch
  os.system(f'cd {repo_name}')
  
  # Make sure that even if the repository is public, the personal token is still in the origin remote url
  if personal_token:
    os.system("git remote set-url origin {}".format(full_url))

  # Add the email and username
  if email: os.system('git config --global user.email "{}"'.format(email))
  if username: os.system('git config --global user.name "{}"'.format(username))
  
  # Bring the public key from the repository and paste it in the authorized_keys
  os.system("mkdir -p ~/.ssh && curl -s -L -f {} {}/{}/.colab_ssh/authorized_keys >> ~/.ssh/authorized_keys".format(
      ("-H 'Authorization: token {}'".format(personal_token)) if personal_token else "",
      repositoryUrl.split(".git")[0].replace("github.com", "raw.githubusercontent.com"), 
      branch))
  
  # Print the VSCode direct link
  try:
    output = get_tunnel_config()
    link = f"vscode://vscode-remote/ssh-remote+root@{output['domain']}:{output['port']}{os.getcwd()}/{repo_name}"
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
      # Support for terminal
      print(f"[Optional] You can open the cloned folder using VSCode, by going to this url:\n{link}")
  except Exception as e:
    if verbose:
      print(e)

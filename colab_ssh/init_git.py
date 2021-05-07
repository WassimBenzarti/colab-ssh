import logging
import os
import sys
import importlib
import re
from urllib.parse import quote
from typing import Optional
from functools import partial

import requests

from colab_ssh.utils.logger import get_logger
from colab_ssh.utils.ui.render_html import render_template
from colab_ssh._command import run_command as _run_command
from .get_tunnel_config import get_tunnel_config, get_argo_tunnel_config
from .utils import show_hint_message


logger = get_logger()


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


repository_regex = re.compile(r"^https://(?P<service>gitlab|github)\.com/(?P<namespace>[^/]+)/(?P<project>[^/]+)\.git$", re.IGNORECASE)


def init_git(repository_url: str,
            branch: Optional[str] = None,
            personal_token: Optional[str] = None,
            email: Optional[str] = None,
            username: Optional[str] = None,
            cloudflared: bool = False,
            verbose: bool = False) -> None:
  if branch is None:
    branch = ""
  repository_info = repository_regex.match(repository_url)
  if repository_info is None:
    raise ValueError("The repository URL must be from Github or Gitlab.")
  repository_info = repository_info.groupdict()
  # Add the Personal access token if available
  full_url = repository_url
  if personal_token is not None:
    if repository_info["service"] == "github":
      full_url = "https://{}@github.com/{}/{}.git".format(
        personal_token,
        repository_info["namespace"],
        repository_info["project"],
      )
    elif repository_info["service"] == "gitlab":
      full_url = "https://oauth2:{}@gitlab.com/{}/{}.git".format(
        personal_token,
        repository_info["namespace"],
        repository_info["project"],
      )
  else:
    response = requests.get(full_url)
    if response.status_code == 200:
      logger.info("✔️ Public repository")
    else:
      # Get username if not passed
      username_input= input(f"Enter your username: (leave it empty if it's '{username}')\n")
      username = quote(username_input or username)
      # Get password
      from getpass import getpass
      password = quote(getpass('Enter your password: \n'))
      if password:
        full_url = "https://{}:{}@{}.com/{}/{}.git".format(
          username, password,
          repository_info["service"],
          repository_info["namespace"],
          repository_info["project"],
        )
  # Clone the repository then add the folder to the sys.path
  _run_command(
      "git clone {} {}".format(
        # Branch argument
        "--branch {}".format(branch) if branch else "",
        # Url argument
        full_url),
      callback=parse_cloning_output
  )

  repo_name = repository_info["project"]

  # Checkout the branch
  os.system(f'cd {repo_name}')

  # Make sure that even if the repository is public, the personal token is still in the origin remote url
  if personal_token is not None:
    os.system("git remote set-url origin {}".format(full_url))

  # Add the email and username
  if email is not None:
    os.system('git config --global user.email "{}"'.format(email))
  if username is not None:
    os.system('git config --global user.name "{}"'.format(username))

  # Bring the public key from the repository and paste it in the authorized_keys
  if repository_info["service"] == "github":
    header = f"-H 'Authorization: token {personal_token}'"
    keys_url = "https://raw.githubusercontent.com/{}/{}/{}/.colab_ssh/authorized_keys".format(
      branch,
      repository_info["namespace"],
      repository_info["project"],
    )
  elif repository_info["service"] == "gitlab":
    # https://docs.gitlab.com/ee/api/README.html#namespaced-path-encoding
    # https://docs.gitlab.com/ee/api/repository_files.html#get-raw-file-from-repository
    header = f"-H 'Authorization: Bearer {personal_token}'"
    keys_url = "https://gitlab.com/api/v4/projects/{}%2F{}/repository/files/.colab_ssh%2Fauthorized_keys/raw?{}".format(
      repository_info["namespace"],
      repository_info["project"],
      f"ref={branch}" if branch else "",
    )
  if personal_token is None:
    header = ""
  os.system(f"mkdir -p ~/.ssh && curl -s -L -f {header} {keys_url} >> ~/.ssh/authorized_keys")

  # Print the VSCode direct link
  try:
    if cloudflared:
      output = get_argo_tunnel_config()
    else:
      output = get_tunnel_config()
    link = f"vscode://vscode-remote/ssh-remote+root@{output['domain']}:{output['port']}{os.getcwd()}/{repo_name}"
    if importlib.util.find_spec("IPython") and 'ipykernel' in sys.modules:
      from IPython.display import HTML, display
      display(HTML(
        render_template("init_git.html", {**output, "link":link, "repo_name":repo_name})
        )
      )
    else:
      # Support for terminal
      print(f"[Optional] You can open the cloned folder using VSCode, by going to this url:\n{link}")
  except Exception as e:
    if verbose:
      print(e)

init_git_cloudflared = partial(init_git, cloudflared=True)
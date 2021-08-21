import abc
from colab_ssh.ssh.public_key import add_to_authorized_keys
import requests


class HTTPSGitProvider(metaclass=abc.ABCMeta):

  def __init__(self, domain):
    self.domain = domain

  def get_public_url(self, namespace, project):
    return "https://{}/{}/{}.git".format(
        self.domain,
        namespace,
        project,
    )

  def get_url_with_pat(
          self, personal_token, namespace, project):
    return "https://{}@{}/{}/{}.git".format(
        personal_token,
        self.domain,
        namespace,
        project,
    )

  def get_url_basic_auth(
          self, username, password, namespace, project):
    return "https://{}:{}@{}/{}/{}.git".format(
        username, password,
        self.domain,
        namespace,
        project,
    )

  def check_repo_exists(self, url):
    response = requests.get(url)
    return response.status_code == 200

  '''
  Takes the following arguments:
    - personal_token: Personal access token
    - namespace: The path to the project or organization
    - project: Project name
    - branch: Branch of the repository
  '''
  @abc.abstractmethod
  def download_keys(
          self, personal_token, namespace, project, branch):
    raise NotImplementedError(
        "Please implement the method download_keys")

  def download_and_store_keys(
          self, personal_token, namespace, project, branch):
    pub_ssh_keys = self.download_keys(
        personal_token, namespace, project, branch)
    add_to_authorized_keys(pub_ssh_keys)

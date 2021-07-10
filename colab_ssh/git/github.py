import requests
from colab_ssh.git.generic import HTTPSGitProvider


class HTTPSGithubProvider(HTTPSGitProvider):
  def download_keys(
          self, personal_token, namespace, project, branch):
    keys_url = "https://raw.githubusercontent.com/{}/{}/{}/.colab_ssh/authorized_keys".format(
        namespace, project, branch, )
    pub_ssh_keys = requests.get(keys_url, headers={
        "Authorization": f"token {personal_token}"
    }, allow_redirects=True).text

    return pub_ssh_keys


github_provider = HTTPSGithubProvider("github.com")

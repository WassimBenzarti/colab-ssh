import requests
from colab_ssh.git.generic import HTTPSGitProvider


class HTTPSGitlabProvider(HTTPSGitProvider):
  def get_url_with_pat(self, personal_token, namespace, project):
    return "https://oauth2:{}@{}/{}/{}.git".format(
        self.domain,
        personal_token,
        namespace,
        project,
    )

  def download_keys(
          self, personal_token, namespace, project, branch):
    # https://docs.gitlab.com/ee/api/README.html#namespaced-path-encoding
    # https://docs.gitlab.com/ee/api/repository_files.html#get-raw-file-from-repository
    headers = {
        "Authorization": "Bearer {personal_token}"} if personal_token else None
    keys_url = "https://gitlab.com/api/v4/projects/{}%2F{}/repository/files/.colab_ssh%2Fauthorized_keys/raw?{}".format(
        namespace, project, f"ref={branch}" if branch else "", )

    return requests.get(keys_url, headers=headers).text


gitlab_provider = HTTPSGitlabProvider("gitlab.com")

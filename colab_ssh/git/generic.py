
import requests


class HTTPSGitProvider:

    def __init__(self, domain):
        self.domain = domain

    def get_public_url(self, namespace, project):
        return "https://{}/{}/{}.git".format(
            self.domain,
            namespace,
            project,
        )

    def get_url_with_pat(self, personal_token, namespace, project):
        return "https://{}@{}/{}/{}.git".format(
            self.domain,
            personal_token,
            namespace,
            project,
        )

    def get_url_basic_auth(self, username, password, namespace, project):
        return "https://{}:{}@{}/{}/{}.git".format(
            username, password,
            self.domain,
            namespace,
            project,
        )

    def check_repo_exists(url):
        response = requests.get(url)
        return response.status_code == 200

    def download_keys(personal_token, namespace, project, branch):
        header = f"-H 'Authorization: token {personal_token}'"
        keys_url = "https://raw.githubusercontent.com/{}/{}/{}/.colab_ssh/authorized_keys".format(
            namespace,
            project,
            branch,
        )

import abc
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
            self.domain,
            personal_token,
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

    def check_repo_exists(url):
        response = requests.get(url)
        return response.status_code == 200

    @abc.abstractmethod
    def download_keys(personal_token, namespace, project, branch):
        raise NotImplementedError(
            "Please implement the method download_keys")


from colab_ssh.repos.generic import HTTPSGitProvider


class HTTPSGitlabProvider(HTTPSGitProvider):
    def get_url_with_pat(self, personal_token, namespace, project):
        return "https://oauth2:{}@{}/{}/{}.git".format(
            self.domain,
            personal_token,
            namespace,
            project,
        )


gitlab_provider = HTTPSGitlabProvider("gitlab.com")

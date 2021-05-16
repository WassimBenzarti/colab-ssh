
from colab_ssh.repos.generic import HTTPSGitProvider


class HTTPSGithubProvider(HTTPSGitProvider):
    def download_keys(personal_token, namespace, project, branch):
        header = f"-H 'Authorization: token {personal_token}'"
        keys_url = "https://raw.githubusercontent.com/{}/{}/{}/.colab_ssh/authorized_keys".format(
            namespace, project, branch, )


github_provider = HTTPSGithubProvider("github.com")

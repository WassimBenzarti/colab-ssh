

def init_git(repositoryUrl,
            branch="master",
            personal_token=None,
            email=None,
            username=None,
            verbose=False):

	full_url = repositoryUrl.replace("github.com", personal_token+"@github.com") if personal_token else repositoryUrl
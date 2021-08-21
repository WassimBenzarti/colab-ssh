
from .github import github_provider
from .gitlab import gitlab_provider

providers = {
    "github": github_provider,
    "gitlab": gitlab_provider,
}


__all__ = [
    "providers"
]

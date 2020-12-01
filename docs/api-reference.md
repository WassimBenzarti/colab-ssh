# API reference


### `launch_ssh_cloudflared` function
This function accepts the following parameters
|Parameter|Type|Required|Default value|Description|
|-|-|-|-|-|
|`password`|string|-|None|The SSH password you want to set, if empty no password will be set. Usually you don't need passwords when you already have an [ssh key setup](../README.md#avoiding-passwords-optional)|
|`verbose`|boolean|-|False|Show more information under the hood|
|`kill_other_processes`|boolean|-|False|This will kill all cloudflared processes before starting a new one|

### `init_git_cloudflared` function
This function allows you to clone a repository (private or public) and sets up the right remote URL without the need for authentication every time you open the notebook, this can be achieved by setting your **github personal token**.

This function accepts the following parameters
|Parameter|Type|Required|Default value|Description|
|-|-|-|-|-|
|repositoryUrl|string|:heavy_check_mark:|-|Your repository URL|
|branch|string|-|`master`|The branch that you want to checkout|
|personal_token|string|Only if you want to clone a private repo or commit to your own repository|-|Your github personal token|
|email|string|Highly recommended if you are going to commit to the repo|-|Your github email. This will automatically set the `git config --global user.email` for you|
|username|string|Highly recommended if you are going to commit to the repo|-|Your github username. This will automatically set the `git config --global user.name` for you|
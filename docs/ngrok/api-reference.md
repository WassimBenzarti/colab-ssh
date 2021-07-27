# API reference


### `launch_ssh` function
This function accepts the following parameters
|Parameter|Type|Required|Default value|Description|
|-|-|-|-|-|
|`token`|string|:heavy_check_mark:|-|Your ngrok token|
|`password`|string|-|None|The SSH password you want to set, if empty no password will be set. Usually you don't need passwords when you already have an [ssh key setup](#avoiding-passwords)|
|`verbose`|boolean|-|False|Show more information under the hood|
|`region`|string|-|`us`|The region you want to setup for ngrok. This can be one of the following: `us`, `eu`, `au`, `ap`, `sa`, `jp`, `in`. See the [official Ngrok documenation](https://ngrok.com/docs#config-options) for more information.|
|`remote_addr`|string|-|None|The reserved remote address. See the [official Ngrok documenation](https://ngrok.com/docs#tcp-remote-addr) for more information.|
|~~`publish`~~|-|-|-|Deprecated|

### `init_git` function
`init_git` allows you to clone a repository (private or public) and sets up the right remote URL without the need for authentication every time you open the notebook, this is achieved by setting your github personal token.

This function accepts the following parameters
|Parameter|Type|Required|Default value|Description|
|-|-|-|-|-|
|repositoryUrl|string|:heavy_check_mark:|-|Your repository URL|
|branch|string|-|`master`|The branch that you want to checkout|
|personal_token|string|Only if you want to clone a private repo or commit to your own repository|-|Your github personal token|
|email|string|Highly recommended if you are going to commit to the repo|-|Your github email. This will automatically set the `git config --global user.email` for you|
|username|string|Highly recommended if you are going to commit to the repo|-|Your github username. This will automatically set the `git config --global user.name` for you|
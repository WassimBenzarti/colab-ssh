# Google Colab-ssh
#### Connect to Google colab via ssh easily

## What is Colab-ssh
Colab-ssh is a light-weight library that enables you to connect to a Google Colab virtual machine using an SSH tunnel.

> You still need to open the Google Colab Notebook interface manually in order to setup this tool. Google Colab doesn't have an API yet to automatically run a notebook for you.

## Getting started
1. Open Google Colab and run this code in one of the code cells
```jupyter
# Install colab_ssh on google colab
!pip install colab_ssh --upgrade

from colab_ssh import launch_ssh, init_git
launch_ssh(ngrokToken,password)

# Optional: if you want to clone a github repository
init_git(githubUrl)
```
- `ngrokToken` is your ngrok token that you can get from [here](https://dashboard.ngrok.com/auth)
- `password` is an optional parameter, this is your ssh password that you want to set.
- `githubUrl` is your github **HTTPS** clone url (usually ends with `.git`)
> Check all the parameters for the `launch_ssh` function in [this section](#API Reference)

### Installation (standalone)
To install Colab-ssh library, you need to run this command
```bash
pip install colab_ssh --upgrade --user
```

### Cloning a repository (Optional)
You probably working on a Github

### Avoiding passwords (Optional)
Instead of setting a password, you can access the SSH tunnel using your own pair of keys.

> **IMPORTANT**: For this to work you need to setup your git repository by using the function `git_init()`

**How it works ?** : We get your **public key** from the repository passed into the `git_init()` function and then we add it to the  `authorized_keys` file (found in `~/.ssh` folder).

You need to follow these steps:
1. Create a pair of SSH key
2. Copy your **public key** (should be inside the file `id_rsa.pub`)
3. In the root of your github repository, create a folder called `.colab_ssh` and a file within it called `authorized_keys`
4. Paste your **public key** inside the file `.collab_ssh/authorized_keys`


### Using VSCode to connect Google Colab
Once you run the code in the **Getting Started** section you will notice a message like this
```
...
Successfully running tcp://0.tcp.ngrok.io:XXXX
...
```
- `XXXX` is the port provided by `ngrok`

You can now open **VSCode** and add this to your SSH Configuration
```
Host google_colab_ssh
  HostName 0.tcp.ngrok.io
  User root
  Port XXXX
```
> Make sure you replace XXXX with the port you just obtained

Then connect to the remote `google_colab_ssh`.

## API Reference

### `launch_ssh` function
This function accepts the following parameters
|Parameter|Type|Required|Default value|Description|
|-|-|-|-|-|
|`token`|string|:heavy_check_mark:|-|Your ngrok token|
|`password`|string|-|None|The SSH password you want to set, if empty no password will be set. Usually you don't need passwords when you already have an [ssh key setup](#avoiding-passwords)|
|`verbose`|boolean|-|False|Show more information under the hood|
|`region`|string|-|`us`|The region you want to setup for ngrok|
|~~`publish`~~|-|-|-|Deprecated|

### `git_init` function
`git_init` allows you to clone a repository (private or public) and sets up the right remote URL without the need for authentication using your github personal token.

This function accepts the following parameters
|Parameter|Type|Required|Default value|Description|
|-|-|-|-|-|
|repositoryUrl|string|:heavy_check_mark:|-|Your repository URL|
|branch|string|-|`master`|The branch that you want to checkout|
|personal_token|string|Only if you want to clone a private repo|-|Your github personal token|
|email|string|Highly recommended if you are going to commit to the repo|-|Your github email. This will automatically set the `git config --global user.email` for you|
|username|string|Highly recommended if you are going to commit to the repo|-|Your github username. This will automatically set the `git config --global user.name` for you|

# Contribution
Well for now, try to discover things yourself.

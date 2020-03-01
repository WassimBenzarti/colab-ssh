# Google Colab-ssh
#### Connect to Google colab via ssh easily

## What is Colab-ssh
Colab-ssh is a light-weight library that enables you to connect to a Google Colab virtual machine using an SSH tunnel.

> User interface is still required in order to create the Colab virtual machine

## Installation
To install Colab-ssh library, you need to run this command
```bash
pip install colab_ssh --upgrade --user
```

## Getting started
1. Open Google Colab and run this code in one of the code cells
```jupyter
# Install colab_ssh
!pip install colab_ssh --upgrade

import colab_ssh import launch_ssh, init_git
launch_ssh(ngrokToken,password)

# Optional: if you want to clone a github repository
init_git(githubUrl)
```

- `password` is your ssh password that you want to choose
- `ngrokToken` is your ngrok token that you can get from [here](https://dashboard.ngrok.com/auth)
- `githubUrl` is your github **HTTPS** clone url (usually ends with `.git`)

### Avoiding passwords
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
Successfully running [b'tcp://0.tcp.ngrok.io:XXXX\n']
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


# Contribution
Well for now, try to discover things yourself.

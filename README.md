# Colab-ssh
#### Connect to Google colab via ssh easily

> 🎉 Happy to announce that we now support VSCode direct links when you use `init_git`

## What is Colab-ssh
Colab-ssh is a light-weight library that enables you to connect to a Google Colab virtual machine using an SSH tunnel.

> <details><summary> <b> Can I open the Colab notebook automatically without user interaction ?</b> </summary>No, you still need to open the Google Colab Notebook interface manually in order to setup this tool. Google Colab doesn't have an API yet to automatically run a notebook for you.</details>

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
> Check all the parameters for the `launch_ssh` function in [this section](#api-reference)

### Cloning a repository (Optional)
If you are a Github fan, you probably want to clone a repository (private or public) to the Google Colab Notebook.
This is why `init_git` is created.

##### What `init_git` does:
- Clones the repository
- Uses your personal token (if you provided it) to setup the repository remote URL (this is useful so you don't have to worry about authentication during `git clone` or `git push` )
- Checkout the branch of your preference
- Sets up the `user.email` and `user.name` for you, in case you need to commit.
- Also, it inserts the cloned folder to the `sys.path`. This is helpful when your cloned repository is a python project and you want to import some python modules directly (without specifying the name of the root folder) to your Google Colab Notebook. Example: If you cloned a repository called `example-repo`. A folder should be created containing your cloned repository. If `example-repo` has a python module called `my_module`, instead of writing in your notebook `import example-repo.my_module`, you can simply do `import my_module`.

#### Example:
```python
init_git("https://github.com/<OWNER>/<REPO_NAME>.git",
         personal_token="<YOUR_GITHUB_PERSONAL_TOKEN>", 
         branch="<YOUR_BRANCH>",
         email="<YOUR_EMAIL>",
         username="<YOUR_USERNAME>")
```
The output of this command will look like this:
```
Successfully cloned the repository
[Optional] You can open the cloned folder using VSCode, by clicking cloned_repo_name
```
The cloned_repo_name will be shown as a link inside the notebook output (or a url in case of a terminal). This is a direct link to open VSCode directly.
> Link doesn't appear or doesn't work?
> - Make sure you have VSCode installed locally for the link to work
> - Make sure that you run `launch_ssh` before `init_git`. The reason for that is because `init_git` shows the link based on the tunnel information provided by the function `launch_ssh`.


### Avoiding passwords (Optional)
Instead of setting a password, you can access the SSH tunnel using your own pair of keys.

> **IMPORTANT**: For this to work you need to setup your git repository by using the function `init_git()`

<details><summary><b>How it works ?</b></summary> 
         
We get your **public key** from the repository passed into the `init_git()` function and then we add it to the  `authorized_keys` file (found in `~/.ssh` folder).
</details>

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
|`region`|string|-|`us`|The region you want to setup for ngrok. This can be one of the following: `us`, `eu`, `au`, `ap`, `sa`, `jp`, `in`. See the [official Ngrok documenation](https://ngrok.com/docs#config-options) for more information.|
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

# Contribution
Start by opening an issue then we can discuss it, we are open for ideas. About the source code documentation, try to discover things yourself for now.

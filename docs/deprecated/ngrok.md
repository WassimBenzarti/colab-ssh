
> :warning: For reasons that exceed the scope of colab-ssh, ngrok doesn't work anymore with Google Colab, Learn more in this issue #45.

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

> Looking for a way to specify an ngrok **region** ? Check all the parameters for the `launch_ssh` function in [this page](api-reference.md)

> Looking for a way to specify an ngrok **reserved remote address** ? Check all the parameters for the `launch_ssh` function in [this page](api-reference.md)

### Cloning a repository (Optional)
If you are a Github fan, you probably want to clone a repository (private or public) to the Google Colab Notebook.
This is why `init_git` is created.

##### What `init_git` does:
- Clones the repository
- Uses your personal token (if you provided it) to setup the repository remote URL (this is useful so you don't have to worry about authentication during `git clone` or `git push`). If you clone a private repository without a personal token, you will be asked to put your password.
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


### Using VSCode to connect to Google Colab
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
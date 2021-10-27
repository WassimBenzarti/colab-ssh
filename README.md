![Cover photo of Colab-ssh](docs/assets/cover.png)

> A new version of colab-ssh is coming soon, stay tuned.

> 🎉 Happy to announce that we now have:
>  - Youtube demo video
>  - Support for Gitlab repositories
>  - VSCode integration with which you can open your VSCode right from the notebook.

# Colab-ssh
Connect to Google colab via ssh easily

[![Downloads](https://pepy.tech/badge/colab-ssh/week)](https://pepy.tech/project/colab-ssh)
[![Downloads](https://pepy.tech/badge/colab-ssh/month)](https://pepy.tech/project/colab-ssh)
[![Downloads](https://pepy.tech/badge/colab-ssh)](https://pepy.tech/project/colab-ssh)

## What is Colab-ssh ?
Colab-ssh is a light-weight library that allows you to connect to Google Colab Notebook using an SSH Tunnel and optionally via VSCode.

## Quick start
You can click on the Google Colab button to clone an already setup notebook:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/WassimBenzarti/colab-ssh/blob/master/docs/Colab_ssh_Initial_project.ipynb)

> :warning: Colab-ssh supports Google colaboratory notebooks only, using it on other notebooks may lead to unexpected behavior. 

## Getting started

Now you can watch a demo video on how to setup Colab-ssh with cloudflared on Youtube. Click the video below to open it.

[![Youtube demo of Colab-ssh](http://img.youtube.com/vi/Q78_MMaNe_U/0.jpg)](http://www.youtube.com/watch?v=Q78_MMaNe_U "Colab-ssh: open Google Colab with VSCode and SSH")

1. Open Google Colab and run this code in one of the code cells
```jupyter
# Install colab_ssh on google colab
!pip install colab_ssh --upgrade

from colab_ssh import launch_ssh_cloudflared, init_git_cloudflared
launch_ssh_cloudflared(password="<PUT_YOUR_PASSWORD_HERE>")

# Optional: if you want to clone a Github or Gitlab repository
repository_url="<PUT_YOUR_REPOSITORY_URL_HERE>"
init_git_cloudflared(repository_url)
```
> Make sure you replace `<PUT_YOUR_PASSWORD_HERE>` with a password of your choice and `<PUT_YOUR_REPOSITORY_URL_HERE>` with the link to your Github/Gitlab repository (if you use the git integration).

The output of this snippet will look similar to the following screenshot:
![launch_ssh_cloudflared output](docs/assets/launch_ssh_cloudflared.jpg)

> :warning: If it's the first time you launch colab-ssh on your machine, it's important to follow the instructions in the **"Client machine configuration" section**. To show the steps that you need to do, **just click "Client machine configuration"**. Don't worry, you don't have to repeat these steps again for each notebook.

> :grey_question: Things doesn't work ? or looking for a way to connect using Ngrok ? Check the [colab-ssh ngrok documentation](docs/ngrok/ngrok.md)


### Cloning a repository (Optional)
If you are a Github/Gitlab fan, you probably want to clone a repository (private or public) repeatedly to the Google Colab Notebook.
This is why `init_git` is created.

<details><summary> <b> What `init_git` does</b></summary>

- Clones the repository
- Uses your personal token (if you provided it) to setup the repository remote URL (this is useful so you don't have to worry about authentication during `git clone` or `git push`). If you clone a private repository without a personal token, you will be asked to put your password (This is only valid for Gitlab, as opposed to Github that recently disabled password authentication).
- Checkout the branch of your preference
- Sets up the `user.email` and `user.name` for you, in case you need to commit.
- Also, it inserts the cloned folder to the `sys.path`. This is helpful when your cloned repository is a python project and you want to import some python modules directly (without specifying the name of the root folder) to your Google Colab Notebook. Example: If you cloned a repository called `example-repo`. A folder should be created containing your cloned repository. If `example-repo` has a python module called `my_module`, instead of writing in your notebook `import example-repo.my_module`, you can simply do `import my_module`.
</details>


#### Example:
```python
init_git_cloudflared("https://github.com/<OWNER>/<REPO_NAME>.git",
         personal_token="<YOUR_GITHUB_PERSONAL_TOKEN>", 
         branch="<YOUR_BRANCH>",
         email="<YOUR_EMAIL>",
         username="<YOUR_USERNAME>")
```
The output of this command will look like this:
![init_git_cloudflared output](docs/assets/init_git_cloudflared.jpg)


This will display a button inside the cell output (or a url in case of a terminal). This is a direct link to open VSCode installed on your machine.
> Link doesn't appear or doesn't work?
> - Make sure you have VSCode installed locally for the link to work
> - Make sure that you run `launch_ssh_cloudflared` before `init_git_cloudflared`. The reason for that is because `init_git_cloudflared` shows the link based on the tunnel information provided by the function `launch_ssh_cloudflared`.

> :warning: Please note that your Gitlab personal access token requires the following scopes: `read_api, read_repository, write_repository`.

### Avoiding passwords (Optional)
Instead of setting a password, you can access the SSH tunnel using your own pair of keys.

> **IMPORTANT**: This feature is only available when you clone your git repository by using the function `init_git_cloudflared()`

You need to follow these steps:
1. Create a pair of SSH key
2. Copy your **public key** (usually it's in the file `~/.ssh/id_rsa.pub`) and make sure you keep your **private key** in a safe place
3. In the root of your github repository, create a folder called `.colab_ssh` and a file within it called `authorized_keys`
4. Paste your **public key** inside the file `.collab_ssh/authorized_keys`
5. Push your changes to the repository and launch the clone again from your Google Colab Notebook

<details><summary><b>How it works behind the scenes ?</b></summary> 
         
We get your **public key** from the repository passed into the `init_git()` function and then we add it to the  `authorized_keys` file (found in `~/.ssh` folder).
</details>

### Other useful documentation
- [Exposing a Google Colab environment variable](docs/expose-env-variable.md)

## API Reference
Check the API reference on this [page](docs/api-reference.md).

## FAQ

<details><summary> <b> Can I open the Colab notebook automatically without user interaction ?</b> </summary>

No, you still need to open the Google Colab Notebook interface manually in order to setup this tool. Google Colab doesn't have an API yet to automatically run a notebook for you.</details>

<details><summary> <b> Some environment variables are available on Google Colab but not available when executing from the terminal ?</b> </summary>

Check out the documentation for how you can [Expose a Google Colab environment variable](docs/expose-env-variable.md).
</details>

# Sponsor this project :)
If you want to buy me a cup of coffee, feel free to reach me or use the following IBAN (International Bank Account Number):
```
TN5904018104003696876646
```

# Contribution
Start by [opening an issue](https://github.com/WassimBenzarti/colab-ssh) so can start working together to enhance the experience of Google Colab users. We would love to hear your ideas!

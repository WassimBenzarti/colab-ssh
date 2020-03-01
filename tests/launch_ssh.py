from colab_ssh import launch_ssh
import os


token = os.environ["NGROK_TOKEN"]
ssh_password = os.environ["SSH_PASSWORD"]

launch_ssh(ssh_password, token)
from colab_ssh.utils.packages.installer import create_deb_installer
from colab_ssh.utils.ui.render_html import render_template
from subprocess import Popen, PIPE
import shlex
from colab_ssh._command import run_command, run_with_pipe
import os
import time
from colab_ssh.get_tunnel_config import get_argo_tunnel_config
from .utils.expose_env_variable import expose_env_variable
import importlib
import sys
import signal

deb_install = create_deb_installer()


def launch_ssh_cloudflared(
               password="",
               verbose=False,
               prevent_interrupt=False,
               kill_other_processes=False):
    # Kill any cloudflared process if running
    if kill_other_processes:
        os.system("kill -9 $(ps aux | grep 'cloudflared' | awk '{print $2}')")

    # Download cloudflared
    if not os.path.isfile("cloudflared"):
        run_command(
            "wget -q -nc https://bin.equinox.io/c/VdrWdbjqyF/cloudflared-stable-linux-amd64.tgz")
        run_command("tar zxf cloudflared-stable-linux-amd64.tgz")
    else:
        if verbose:
            print("DEBUG: Skipping cloudflared installation")

    # Install the openssh server
    deb_install("openssh-server", verbose=verbose)

    # Set the password
    run_with_pipe("echo root:{} | chpasswd".format(password))

    # Configure the openSSH server
    run_command("mkdir -p /var/run/sshd")
    os.system("echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config")
    if password:
        os.system('echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config')

    expose_env_variable("LD_LIBRARY_PATH")
    expose_env_variable("COLAB_TPU_ADDR")
    expose_env_variable("COLAB_GPU")
    expose_env_variable("TBE_CREDS_ADDR")
    expose_env_variable("TF_FORCE_GPU_ALLOW_GROWTH")
    expose_env_variable("TPU_NAME")
    expose_env_variable("XRT_TPU_CONFIG")

    os.system('service ssh start')

    extra_params = []
    info = None

    # Prepare the cloudflared command
    popen_command = f'./cloudflared tunnel --url ssh://localhost:22 --logfile ./cloudflared.log --metrics localhost:45678 {" ".join(extra_params)}'
    preexec_fn = None
    if prevent_interrupt:
        popen_command = 'nohup ' + popen_command
        preexec_fn = os.setpgrp
    popen_command = shlex.split(popen_command)

    # Initial sleep time
    sleep_time = 2.0

    # Create tunnel and retry if failed
    for i in range(10):
        proc = Popen(popen_command, stdout=PIPE, preexec_fn=preexec_fn)
        if verbose:
            print(f"DEBUG: Cloudflared process: PID={proc.pid}")
        time.sleep(sleep_time)
        try:
            info = get_argo_tunnel_config()
            break
        except Exception as e:
            os.kill(proc.pid, signal.SIGKILL)
            if verbose:
                print(f"DEBUG: Exception: {e.args[0]}")
                print(f"DEBUG: Killing {proc.pid}. Retrying...")
        # Increase the sleep time and try again
        sleep_time *= 1.5

    if verbose:
        print("DEBUG:", info)

    if info:
        # print("Successfully running on ", "{}:{}".format(host, port))
        if importlib.util.find_spec("IPython") and 'ipykernel' in sys.modules:
            from IPython.display import display, HTML
            display(HTML(render_template("launch_ssh_cloudflared.html", info)))
        else:
            print("Now, you need to setup your client machine by following these steps:")
            print("""
    1) Download Cloudflared (Argo Tunnel) from https://developers.cloudflare.com/argo-tunnel/getting-started/installation, then copy the absolute path to the cloudflare binary.
    2) Append the following to your SSH config file (usually under ~/.ssh/config):

        Host *.trycloudflare.com
            HostName %h
            User root
            Port 22
            ProxyCommand <PUT_THE_ABSOLUTE_CLOUDFLARE_PATH_HERE> access ssh --hostname %h

*) Connect with SSH Terminal
    To connect using your terminal, type this command:
        ssh {domain}

*) Connect with VSCode Remote SSH
    You can also connect with VSCode Remote SSH (Ctrl+Shift+P and type "Connect to Host..."). Then, paste the following hostname in the opened command palette:
        {domain}
""".format(**info))

    #     print("[Optional] You can also connect with VSCode SSH Remote extension by:")
    #     print(f"""
    # 1. Set the following configuration into your SSH config file (~/.ssh/config):

    #     Host *.trycloudflare.com
    #         HostName %h
    #         User root
    #         Port {port}
    #         ProxyCommand <PUT_THE_ABSOLUTE_CLOUDFLARE_PATH_HERE> access ssh --hostname %h

    # 2. Connect to Remote SSH on VSCode (Ctrl+Shift+P and type "Connect to Host...") and paste this hostname:
    #     {host}
    #     """)
    #     print(f'''

        #   ''')
    else:
        print(proc.stdout.readlines())
        raise Exception(
            "It looks like something went wrong, please make sure your token is valid")
    proc.stdout.close()

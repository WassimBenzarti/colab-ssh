import re
import time
from subprocess import PIPE, Popen

from colab_ssh._command import run_command
from colab_ssh.launch_ssh_cloudflared import launch_ssh_cloudflared


def launch_ssh_pinggy(password="",
                      verbose=False,
                      prevent_interrupt=False,
                      kill_other_processes=True):
  """
  Launch an SSH server and expose it through a free Pinggy TCP tunnel.

  Same parameters and password-based authentication as launch_ssh_cloudflared,
  but the tunnel is a plain reverse SSH connection, so no extra binary is
  needed on the client: just `ssh -p PORT root@HOST`.
  """
  # Reuse cloudflared's SSH setup (installs openssh-server, sets the
  # password, configures sshd, exposes env vars, starts ssh).
  # Temporarily silence its tunnel output by pointing the tunnel config
  # reader at a fresh log: launch_ssh_cloudflared starts cloudflared itself,
  # so instead we only need its setup part. To keep this simple we start
  # sshd here with the same steps as launch_ssh_cloudflared but without a
  # cloudflared tunnel.
  from colab_ssh.utils.packages.installer import create_deb_installer
  from .utils.expose_env_variable import expose_env_variable
  from colab_ssh._command import run_with_pipe

  deb_install = create_deb_installer()

  if kill_other_processes:
    run_command("pkill -f pinggy 2>/dev/null || true")

  deb_install("openssh-server", verbose=verbose)

  run_with_pipe("echo root:{} | chpasswd".format(password))

  run_command("mkdir -p /var/run/sshd")
  run_command("echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config")
  if password:
    run_command('echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config')

  expose_env_variable("LD_LIBRARY_PATH")
  expose_env_variable("COLAB_TPU_ADDR")
  expose_env_variable("COLAB_GPU")
  expose_env_variable("TBE_CREDS_ADDR")
  expose_env_variable("TF_FORCE_GPU_ALLOW_GROWTH")
  expose_env_variable("TPU_NAME")
  expose_env_variable("XRT_TPU_CONFIG")

  run_command('service ssh start')

  open('pinggy.log', 'w').close()
  proc = Popen(
      ['ssh', '-T', '-p', '443',
       '-o', 'StrictHostKeyChecking=accept-new',
       '-o', 'ServerAliveInterval=30', '-o', 'ServerAliveCountMax=3',
       '-o', 'ExitOnForwardFailure=yes',
       '-R', '0:localhost:22', 'tcp@free.pinggy.io'],
      stdout=PIPE, stderr=PIPE, universal_newlines=True)

  time.sleep(4)
  if proc.poll() is not None:
    raise Exception(
        "Pinggy tunnel exited unexpectedly:\n{}".format(
            proc.stderr.read()[-1500:]))

  if verbose:
    print("Pinggy process: PID={}".format(proc.pid))
  print("Pinggy tunnel is running. Connection details are in pinggy.log.")
  return proc

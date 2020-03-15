import random, string
from subprocess import Popen, PIPE
import shlex
from colab_ssh._command import run_command, run_with_pipe
import os
import time
import requests
import re


def launch_ssh(token, password="", publish=True):

  # Ensure the ngrok auth token is not empty
  if(not token):
    raise "Ngrok AuthToken is missing, copy it from https://dashboard.ngrok.com/auth"

  # Kill any ngrok process if running
  os.system("kill $(ps aux | grep 'ngrok' | awk '{print $2}')")

  # Download ngrok
  run_command("wget -q -nc https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip")
  run_command("unzip -qq -n ngrok-stable-linux-amd64.zip")

  # Install the openssh server
  os.system("apt-get -qq install -o=Dpkg::Use-Pty=0 openssh-server pwgen > /dev/null")

  # Set the password
  run_with_pipe("echo root:{} | chpasswd".format(password))

  # Configure the openSSH server
  run_command("mkdir -p /var/run/sshd")
  os.system("echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config")
  if password:
    os.system('echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config')
  os.system('echo "LD_LIBRARY_PATH=/usr/lib64-nvidia" >> /root/.bashrc')
  os.system('echo "export LD_LIBRARY_PATH" >> /root/.bashrc')
  os.system('/usr/sbin/sshd -D &')

  # Create tunnel
  Popen(shlex.split('./ngrok tcp --authtoken {} 22'.format(token)), stdout=PIPE,stderr=PIPE,stdin=PIPE)
  time.sleep(4)

  # Get public address
  info = run_with_pipe('''curl http://localhost:4040/api/tunnels | python3 -c "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])"''')
  
  if publish and info and info[0]:
    publish_host(info[0].decode().strip())

  if info[0]:
    # Extract the host and port
    host_and_port = re.match(r'.*://(.*):(\d+)\n', info[0].decode())
    host = host_and_port.group(1)
    port = host_and_port.group(2)
    print("Successfully running", "{}:{}".format(host,port))
    print("[Optional] You can also connect with VSCode SSH Remote extension using this configuration:")
    print('''
      Host google_colab_ssh
          HostName 0.ssh.ngrok.io
          User root
          Port {}
      '''.format(port))
  else:
    print("It looks like something went wrong, please try again.")

  

  return info
  

def publish_host(address):
  url = 'https://api.jsonbin.io/b/5e5faa9b763fa966d40ed31b'
  headers = {'Content-Type': 'application/json'}
  data = {"host": address}

  req = requests.put(url, json=data, headers=headers)
  # print("Published the host, See the vscode extension: ",req.text)
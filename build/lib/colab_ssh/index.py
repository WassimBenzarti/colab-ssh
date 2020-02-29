import random, string
from subprocess import Popen, PIPE
import shlex

def run_command(command):
  process = Popen(shlex.split(command), stdout=PIPE, universal_newlines=True)
  while True:
      output = process.stdout.readline()
      if output == '' and process.poll() is not None:
          break
      if output:
          print(output.strip())
  rc = process.poll()
  return rc

def run_with_pipe(command):
  commands = list(map(shlex.split,command.split("|")))
  ps = Popen(commands[0], stdout=PIPE)
  for command in commands[1:]:
    ps = Popen(command, stdin=ps.stdout,stdout=PIPE)
  return ps.stdout.readlines()


def launch_ssh(password, token):
  #Download ngrok
  run_command("wget -q -nc https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip")
  run_command("unzip -qq -n ngrok-stable-linux-amd64.zip")
  run_command("apt-get install -qq -o=Dpkg::Use-Pty=0 openssh-server pwgen > /dev/null")
  run_command("echo root:$password | sudo chpasswd")
  run_command("mkdir -p /var/run/sshd")
  run_command("echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config")
  run_command('echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config')
  run_command('echo "LD_LIBRARY_PATH=/usr/lib64-nvidia" >> /root/.bashrc')
  run_command('echo "export LD_LIBRARY_PATH" >> /root/.bashrc')
  get_ipython().system_raw('/usr/sbin/sshd -D &')
  print("Copy authtoken from https://dashboard.ngrok.com/auth")
  import getpass
  authtoken = token

  #Create tunnel
  get_ipython().system_raw('./ngrok authtoken $authtoken && ./ngrok tcp 22 &')
  #Print root password
  print("Root password: {}".format(password))
  #Get public address
  info = run_with_pipe('''curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])"''')

  print("Successfully running", info[0].decode())
  
launch_ssh("123456","3jwLpGRs2V2jsM4A2Yiy_y6wLvFcDJ6L4q6rVGuC5")
import random, string

from colab_ssh._command import run_command, run_with_pipe



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
  


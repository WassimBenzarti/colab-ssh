import random
import string
from subprocess import Popen, PIPE
import shlex
from colab_ssh._command import run_command, run_with_pipe
import os
import time
import requests
import re
from colab_ssh.get_tunnel_config import get_tunnel_config
from .utils.expose_env_variable import expose_env_variable


def launch_ssh(token, password="", publish=True, verbose=False, region="us"):

	# Ensure the ngrok auth token is not empty
	if(not token):
		raise Exception(
			"Ngrok AuthToken is missing, copy it from https://dashboard.ngrok.com/auth")

	if(not region):
		raise Exception("Region is required. If you do want prefer the default value, don't set the 'region' parameter")

	# Kill any ngrok process if running
	os.system("kill $(ps aux | grep 'ngrok' | awk '{print $2}')")

	
	# Download ngrok
	run_command(
		"wget -q -nc https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip")
	run_command("unzip -qq -n ngrok-stable-linux-amd64.zip")

	# Install the openssh server
	os.system(
		"apt-get -qq install -o=Dpkg::Use-Pty=0 openssh-server pwgen > /dev/null")

	# Set the password
	run_with_pipe("echo root:{} | chpasswd".format(password))

	# Configure the openSSH server
	run_command("mkdir -p /var/run/sshd")
	os.system("echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config")
	if password:
		os.system('echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config')

	expose_env_variable("LD_LIBRARY_PATH")
	expose_env_variable("COLAB_TPU_ADDR")

	os.system('/usr/sbin/sshd -D &')

	# Create tunnel
	proc = Popen(shlex.split('./ngrok tcp --authtoken {} --region {} 22'.format(token, region)), stdout=PIPE)
	

	time.sleep(4)
	# Get public address
	try:
		info = get_tunnel_config()
	except:
		raise Exception("It looks like something went wrong, please make sure your token is valid")

	if verbose:
		print("DEBUG:", info)

	if info:
		# Extract the host and port
		host = info["domain"]
		port = info["port"]
		print("Successfully running", "{}:{}".format(host, port))
		print("[Optional] You can also connect with VSCode SSH Remote extension using this configuration:")
		print(f'''
	Host google_colab_ssh
		HostName {host}
		User root
		Port {port}
	  ''')
	else:
		print(proc.stdout.readlines())
		raise Exception(
			"It looks like something went wrong, please make sure your token is valid")
	proc.stdout.close()



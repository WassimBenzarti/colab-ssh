import os



def launch_ssh_home(ip_address, reverse_ports=[]):
	
	# Kill all ssh intances including the server
	os.system("pkill -f ssh")

	# Download autossh
	os.system("apt-get install -y autossh openssh-server")

	# Permit the root login
	os.system("echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config")

	# Launch the SSH Server
	os.system('/usr/sbin/sshd -D &')
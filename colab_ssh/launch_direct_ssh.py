import os



def launch_direct_ssh(username, ip_address, port, 
		reverse_ports=["6022:127.0.0.1:22"], 
		public_key_path="%USERPROFILE%/.ssh/id_rsa.pub"):
	"""
	Launches a direct ssh connection
	! IMPORTANT ! This requires that you install openssh-server locally on your machine and
	open your SSH port (and make sure it's publically available on the internet)
	Arguments
		username: The username that you want to connect with (your computer's username)
		ip_address: The ip address to your machine
		port: The port where openssh-server is listening
		reverse_ports: This is used when you want to forward a port to your machine.
			Use this format <remoteport>:127.0.0.1:<localport>
		public_key_path: Public key path (Please change it to '~/.ssh/id_rsa.pub' if you are on linux)
	"""
	# Kill all ssh intances including the server
	os.system("pkill -f ssh")

	# Download autossh
	os.system("apt-get install -y autossh openssh-server")

	# Get the public key from the client (the one with the ip_address)
	os.system(f"scp -P {port} {username}@{ip_address}:{public_key_path} ~/.ssh/authorized_keys")

	# Permit the root login
	os.system("echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config")

	# Launch the SSH Server
	os.system('/usr/sbin/sshd -D &')

	# Launch the connection
	# Prepare the ports
	reverse_tunnel_ports = " -R ".join(reverse_ports)
	if len(reverse_ports) >0:
		reverse_tunnel_ports = " -R "+reverse_tunnel_ports
	os.system(f'autossh -o "ServerAliveInterval=1" -o "StrictHostKeyChecking=no" -f -T -N {reverse_tunnel_ports} {username}@{ip_address} -p {port}')
import os

def set_private_key(private_key,filename="/root/.ssh/id_rsa"):
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	with open(filename, "w") as f:
  		f.write(private_key)
	os.chmod(filename, 0o600)

	os.system("ssh-keygen -y -f ~/.ssh/id_rsa >> ~/.ssh/id_rsa.pub")
	print("Private key added successfully")
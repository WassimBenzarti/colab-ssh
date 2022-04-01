import paramiko
from paramiko import SSHClient


def execute_remote_command(
        domain, port, command="ls -l", username="root",
        password=None):
  client = SSHClient()
  client.set_missing_host_key_policy(
      paramiko.AutoAddPolicy())
  client.connect(domain, port,
                 username=username,
                 password=password)
  stdin, stdout, stderr = client.exec_command(command)
  stdout = stdout.read().decode().strip()
  stderr = stderr.read().decode().strip()
  client.close()
  if stderr:
    raise Exception(
        f"There was an error in the remote command: {stderr}")
  return stdout

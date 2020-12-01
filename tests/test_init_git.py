import builtins
import getpass
import logging
from colab_ssh import launch_ssh
import os
from colab_ssh import init_git_cloudflared
import mock

def test_init_git():
	os.chdir("/tmp")
	init_git_cloudflared(
		"https://github.com/WassimBenzarti/colab-ssh-connector.git",
		verbose=True
	)

def test_private_git_repo_no_credentials(capsys, caplog):
	caplog.set_level(logging.ERROR, logger="git")
	private_repo = "https://github.com/WassimBenzarti/my-cv.git"
	with mock.patch.object(builtins, 'input', lambda x: "\n"):
		with mock.patch.object(getpass, 'getpass', lambda x: ''):
			init_git_cloudflared(private_repo)
	
	assert "No such device or address" in caplog.text
	output = capsys.readouterr()
	assert "You probably have to enter your username and password" in output.out
 	
def test_private_git_repo_wrong_credentials(capsys, caplog):
	caplog.set_level(logging.ERROR, logger="git")
	private_repo = "https://github.com/WassimBenzarti/my-cv.git"
	with mock.patch.object(builtins, 'input', lambda x: 'hello'):
		with mock.patch.object(getpass, 'getpass', lambda x: '123'):
			init_git_cloudflared(private_repo)
	
	assert "Invalid username or password" in caplog.text
	output = capsys.readouterr()
	assert "Please check your username and password" in output.out
 	

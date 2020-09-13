from colab_ssh import launch_ssh
import os
from colab_ssh import init_git


def test_init_git():
	os.chdir("/tmp")
	init_git(
		"https://github.com/WassimBenzarti/colab-ssh-connector.git",
		verbose=True
	)

from colab_ssh import launch_ssh
import unittest
import os
from colab_ssh import init_git

class TestInitGit(unittest.TestCase):

	def test_init_git(self):
		os.chdir("/tmp")
		init_git(
			"https://github.com/WassimBenzarti/colab-ssh-connector.git",
			verbose=True
		)

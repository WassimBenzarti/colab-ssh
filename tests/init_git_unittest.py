from unittest.mock import patch, call
from colab_ssh import launch_ssh
from io import StringIO
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

	@patch('sys.stdout', new_callable=StringIO)
	def test_with_private_repository(self, mock_stdout):
		private_repo = "https://github.com/WassimBenzarti/my-cv.git"
		init_git(private_repo)
		assert mock_stdout.getValue() == """Error: fatal: could not read Username for 'https://github.com': No such device or address

			Hint: You probably have to enter your username and password
"""
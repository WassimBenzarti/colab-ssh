import unittest
from colab_ssh.utils import expose_env_variable

class TestLaunchSSH(unittest.TestCase):

	def test_env_var(self):
		expose_env_variable("PATH")

		with open("/root/.bashrc", "r") as f:
			last_line = f.readlines()[-1]
			self.assertIn("export PATH=", last_line)

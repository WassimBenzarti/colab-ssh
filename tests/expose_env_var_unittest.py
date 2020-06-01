import unittest
import os
from colab_ssh.utils import expose_env_variable

class TestLaunchSSH(unittest.TestCase):
	# Since we cannot access /root/.bashrc on Github Actions
	
	def setUp(self):
		self.bash_rc_path = "./.bashrc"

	def test_env_var(self):
		
		os.system(f"echo 'previous stuff' >> {self.bash_rc_path}")
		os.environ["COLAB_SSH_TEST_ENV_VAR"] = "123"
		
		expose_env_variable("COLAB_SSH_TEST_ENV_VAR", bash_rc_path=self.bash_rc_path)

		with open("./.bashrc", "r") as f:
			lines = f.readlines()
			self.assertEqual(lines,[
				"previous stuff\n",
				"export COLAB_SSH_TEST_ENV_VAR=123\n"
			])
		
	def tearDown(self):
		os.remove(self.bash_rc_path)

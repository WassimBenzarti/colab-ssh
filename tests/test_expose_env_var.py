import os
from pytest import fixture
from colab_ssh.utils import expose_env_variable


@fixture()
def bash_rc_path():
	bash_rc_path = "./.bashrc"
	yield bash_rc_path
	os.remove(bash_rc_path)

def test_env_var(bash_rc_path):
	
	os.system(f"echo 'previous stuff' >> {bash_rc_path}")
	os.environ["COLAB_SSH_TEST_ENV_VAR"] = "123"
	
	expose_env_variable("COLAB_SSH_TEST_ENV_VAR", bash_rc_path)

	with open("./.bashrc", "r") as f:
		lines = f.readlines()
		assert lines == [
			"previous stuff\n",
			"export COLAB_SSH_TEST_ENV_VAR=123\n"
		]


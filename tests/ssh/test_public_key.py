import pathlib
import shutil
from pytest import fixture

from colab_ssh.ssh.public_key import add_to_authorized_keys


@fixture
def ssh_directory():
  dir_path = pathlib.Path(
      "/tmp", ".ssh")
  dir_path.mkdir(parents=True, exist_ok=True)
  yield dir_path
  shutil.rmtree(dir_path)


def test_add_to_authorized_keys(ssh_directory):

  fake_pub_keys = '''
ssh-rsa 123
ssh-rsa 456
'''

  add_to_authorized_keys(fake_pub_keys, ssh_directory)

  with open(ssh_directory.joinpath("authorized_keys"), "r") as f:
    public_keys = f.read()
    assert fake_pub_keys in public_keys 

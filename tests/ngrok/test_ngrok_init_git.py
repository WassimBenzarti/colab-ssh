import shutil
import pytest
import builtins
import getpass
import logging
from colab_ssh import launch_ssh
import os
from colab_ssh import init_git
import mock


@pytest.fixture
def temporary_clone():
  os.chdir("/tmp")
  yield "/tmp/colab-ssh"
  shutil.rmtree("/tmp/colab-ssh", ignore_errors=True)


def test_init_git(temporary_clone):
  os.chdir("/tmp")
  init_git(
      "https://github.com/WassimBenzarti/colab-ssh.git",
      verbose=True
  )
  isDirectory = os.path.isdir("/tmp/colab-ssh")
  assert isDirectory == True


def test_private_git_repo_no_credentials(
        capsys, caplog, temporary_clone):
  caplog.set_level(logging.ERROR, logger="git")
  private_repo = "https://github.com/WassimBenzarti/my-cv.git"
  with pytest.raises(Exception) as clone_err:
    with mock.patch.object(builtins, 'input', lambda x: "\n"):
      with mock.patch.object(getpass, 'getpass', lambda x: ''):
        init_git(private_repo, verbose=True)

  assert "Cannot clone the project, the git clone command failed" in str(
      clone_err)
  assert "No such device or address" in caplog.text
  output = capsys.readouterr()
  assert "You probably have to enter your username and password" in output.out


def test_private_git_repo_wrong_credentials(
        capsys, caplog, temporary_clone):
  caplog.set_level(logging.ERROR, logger="git")
  private_repo = "https://github.com/WassimBenzarti/my-cv.git"
  with pytest.raises(Exception) as clone_err:
    with mock.patch.object(builtins, 'input', lambda x: 'hello'):
      with mock.patch.object(getpass, 'getpass', lambda x: '123'):
        init_git(private_repo)
  assert "Cannot clone the project, the git clone command failed" in str(
      clone_err)
  assert "Support for password authentication was removed on" in caplog.text
  output = capsys.readouterr()
  assert "Support for password authentication was removed from github" in output.out

import pytest
import builtins
import getpass
import logging
import os
import mock

from colab_ssh import launch_ssh
from colab_ssh import init_git_cloudflared


def test_public_repo_github():
  os.chdir("/tmp")
  init_git_cloudflared(
      "https://github.com/WassimBenzarti/colab-ssh.git",
      verbose=True
  )


def test_public_repo_gitlab():
  os.chdir("/tmp")
  init_git_cloudflared(
      "https://gitlab.com/ldgarciac/colab-ssh-test-public",
      verbose=True
  )


def private_git_repo_no_credentials(capsys, caplog, private_repo):
  caplog.set_level(logging.ERROR, logger="git")
  with pytest.raises(Exception) as clone_err:
    with mock.patch.object(builtins, 'input', lambda x: "\n"):
      with mock.patch.object(getpass, 'getpass', lambda x: ''):
        init_git_cloudflared(private_repo)

  assert "No such device or address" in caplog.text
  output = capsys.readouterr()
  assert "You probably have to enter your username and password" in output.out


def test_private_git_repo_no_credentials_github(capsys, caplog):
  private_git_repo_no_credentials(
      capsys, caplog,
      "https://github.com/WassimBenzarti/my-cv.git")


def test_private_git_repo_no_credentials_gitlab(capsys, caplog):
  private_git_repo_no_credentials(
      capsys, caplog,
      "https://gitlab.com/ldgarciac/colab-ssh-test-private.git")


def private_git_repo_wrong_credentials(
        capsys, caplog, private_repo):
  caplog.set_level(logging.ERROR, logger="git")
  with pytest.raises(Exception):
    with mock.patch.object(builtins, 'input', lambda x: 'hello'):
      with mock.patch.object(getpass, 'getpass', lambda x: '123'):
        init_git_cloudflared(private_repo)

  return caplog

  #assert "Support for password authentication was removed on" in caplog.text
  #output = capsys.readouterr()
  #assert "Support for password authentication was removed from github" in output.out


def test_private_git_repo_wrong_credentials_github(
        capsys, caplog):
  log = private_git_repo_wrong_credentials(
      capsys, caplog,
      "https://github.com/WassimBenzarti/my-cv.git")
  assert "Support for password authentication was removed on" in log.text
  output = capsys.readouterr()
  assert "Support for password authentication was removed from github" in output.out


def test_private_git_repo_wrong_credentials_gitlab(
        capsys, caplog):
  log = private_git_repo_wrong_credentials(
      capsys, caplog,
      "https://gitlab.com/ldgarciac/colab-ssh-test-private.git")
  assert (
      "Invalid username or password" in log.text
      or "HTTP Basic: Access denied" in log.text
  )
  output = capsys.readouterr()
  assert "Please check your username and password" in output.out

import pytest
from colab_ssh.utils import execute_remote_command


def pytest_collection_modifyitems(items):
  for item in items:
    if item.get_marker('timeout') is None:
      item.add_marker(pytest.mark.timeout(30))


@pytest.fixture
def ssh_check():
  def _ssh_check(domain, port):
    output = execute_remote_command(
        domain, port, command="echo hello world")
    assert output == "hello world"

  yield _ssh_check

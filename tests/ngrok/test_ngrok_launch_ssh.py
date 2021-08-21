from colab_ssh import launch_ssh
import os
import pytest
from dotenv import load_dotenv


@pytest.fixture
def ngorkToken():
  load_dotenv(verbose=True)
  token = os.getenv("NGROK_TOKEN")
  if(not token):
    raise Exception(
        "Missing NGROK_TOKEN in the environment, you add it to a .env file in the root folder.")
  yield token

@pytest.fixture
def clean_ngrok_tunnel():
    yield
    os.system("kill $(ps aux | grep '\\.\\/ngrok tcp' | awk '{print $2}')")


def test_token_is_wrong(capsys, caplog):
  with pytest.raises(Exception) as e:
    launch_ssh(", ")
  exception = e.value
  assert str(
      exception) == "It looks like something went wrong, please make sure your token is valid"


def test_token_missing(capsys, caplog):
  with pytest.raises(Exception) as e:
    launch_ssh("")
  exception = e.value
  assert str(
      exception) == "Ngrok AuthToken is missing, copy it from https://dashboard.ngrok.com/auth"


def test_success(ngorkToken, capsys, caplog, clean_ngrok_tunnel):
  launch_ssh(ngorkToken, verbose=True)


def test_success_with_region(ngorkToken, capsys, caplog, clean_ngrok_tunnel):
  launch_ssh(ngorkToken, verbose=True, region="eu")

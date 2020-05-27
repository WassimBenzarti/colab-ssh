from colab_ssh import launch_ssh
import unittest
import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

NGROK_TOKEN = os.getenv("NGROK_TOKEN")

class TestLaunchSSH(unittest.TestCase):

    def test_token_is_wrong(self):
        with self.assertRaises(Exception) as e:
            launch_ssh(", ")
        exception = e.exception
        self.assertEqual(str(exception), "It looks like something went wrong, please make sure your token is valid")

    def test_token_missing(self):
        with self.assertRaises(Exception) as e:
            launch_ssh("")
        exception = e.exception
        self.assertEqual(str(exception), "Ngrok AuthToken is missing, copy it from https://dashboard.ngrok.com/auth")


    def test_success(self):
        launch_ssh(NGROK_TOKEN, verbose=True)

    def test_success_with_region(self):
        launch_ssh(NGROK_TOKEN, verbose=True, region="eu")


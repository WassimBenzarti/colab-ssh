from colab_ssh import launch_ssh
import unittest
import os

print(os.environ.get("NGROK_TOKEN"))
NGROK_TOKEN = os.getenv("NGROK_TOKEN")
print(NGROK_TOKEN)
class TestLaunchSSH(unittest.TestCase):

    def test_token_missing(self):
        with self.assertRaises(Exception):
            launch_ssh()

    def test_success(self):
        launch_ssh(NGROK_TOKEN, verbose=True)

    
        

if __name__ == '__main__':
    unittest.main()
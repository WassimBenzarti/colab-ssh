import unittest
from colab_ssh import init_git


class TestGit(unittest.TestCase):

    def test_first(self):
        invoked = 0
        def callback(output):
            global invoked
            invoked = 1
            
        init_git("https://github.com/WassimBenzarti/colab-ssh-connector.git")

        self.assertTrue(invoked > 0,"invoked < 0")


if __name__ == '__main__':
    unittest.main()
from colab_ssh import launch_ssh_cloudflared


def test_success():
  launch_ssh_cloudflared("123456", verbose=True)


def test_success_without_password():
  launch_ssh_cloudflared(verbose=True)

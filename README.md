# Google CoLab SSH
Connect to Google colab via ssh easily

## Installation
```bash
pip install colab_ssh --upgrade --user
```

## Getting started

```python
import colab_ssh import launch_ssh
launch_ssh(password, ngrokToken)
```

`password` is your ssh password that you want to choose
`ngrokToken` is your ngrok token that you can get from [here](https://dashboard.ngrok.com/auth)
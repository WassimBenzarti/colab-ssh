from colab_ssh.utils.expose.expose_iframe import expose_iframe
from logging import Logger
import logging
from .launch_dashboard import launch_dashboard
from .web_server import launch_api_server
from colab_ssh.utils.logger.logger import get_logger


def create_colab_launch_dashboard():
	logger = get_logger()
	logger.setLevel(logging.DEBUG)
	return launch_dashboard(
		expose_view=expose_iframe, 
		launch_server=launch_api_server,
		logger=logger
		)
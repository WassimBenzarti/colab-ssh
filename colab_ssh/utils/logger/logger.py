import logging

formatter = logging.Formatter("[%(name)s::%(levelname)s] %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)

def get_logger(name="colab-ssh"):
	logger = logging.getLogger(name)
	#logger.propagate = False
	logger.handlers.clear()
	logger.addHandler(handler)
	return logger



from google.colab.output import eval_js


def expose_port(port):
	if port is None:
		raise Exception("Port is missing")
	return eval_js(f"google.colab.kernel.proxyPort({port})")
from google.colab.output import serve_kernel_port_as_iframe

def expose_iframe(port, **kwargs):
	if port is None:
		raise Exception("Port is missing")

	serve_kernel_port_as_iframe(port, **kwargs)
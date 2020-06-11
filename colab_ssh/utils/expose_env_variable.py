import os

def expose_env_variable(
	env_variable_name, 
	file_path="/etc/environment"):
	if env_variable_name in os.environ:
		os.system(f'echo "export {env_variable_name}=${env_variable_name}" >> {file_path}')

import os

def expose_env_variable(
	env_variable_name, 
	bash_rc_path="/root/.bashrc"):
	if env_variable_name in os.environ:
		os.system(f'echo "export {env_variable_name}=${env_variable_name}" >> {bash_rc_path}')
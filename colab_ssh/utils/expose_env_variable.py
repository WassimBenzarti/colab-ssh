import os

def expose_env_variable(env_variable_name):
	os.system(f'echo "export {env_variable_name}=${env_variable_name}" >> /root/.bashrc')
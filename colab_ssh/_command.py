from subprocess import Popen, PIPE
import shlex


def run_command(command, callback=None):
	with Popen(shlex.split(command), stdout=PIPE, stderr=PIPE, universal_newlines=True) as process:
		while True:
			output = process.stdout.readline()
			if output == '' and process.poll() is not None:
				break
			if output:
				print(output.strip())
		rc = process.poll()
		if rc is None:
			process.kill()
		if callback:
			error_output = process.stderr.readlines()
			callback(error_output)
		
		process.stdout.close()
		process.stderr.close()
		process.terminate()
	return rc


def run_with_pipe(command):
	commands = list(map(shlex.split, command.split("|")))
	ps = Popen(commands[0], stdout=PIPE, stderr=PIPE)
	for command in commands[1:]:
		ps_new = Popen(command, stdin=ps.stdout, stdout=PIPE, stderr=PIPE)
		ps.stdout.close()
		ps.stderr.close()
		ps.wait()
		ps = ps_new

	result = ps.stdout.readlines()
	ps.stdout.close()
	ps.stderr.close()
	ps.wait()
	return result

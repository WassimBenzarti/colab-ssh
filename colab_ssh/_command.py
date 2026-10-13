import subprocess
import shlex
import os
import signal


def run_command(command, callback=None):
  """Run a command and stream stdout. Returns the exit code."""
  with subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        universal_newlines=True) as process:
    while True:
      output = process.stdout.readline()
      if output == '' and process.poll() is not None:
        break
      if output:
        print(output.strip())
    rc = process.poll()
    if callback:
      error_output = process.stderr.readlines()
      callback(error_output)
    process.stdout.close()
    process.stderr.close()
  return rc


def stop_process_group(pid):
  """Terminate a process group and its children with SIGTERM."""
  try:
    os.killpg(pid, signal.SIGTERM)
  except (ProcessLookupError, OSError):
    pass


def run_with_pipe(command):
  commands = list(map(shlex.split, command.split("|")))
  ps = subprocess.Popen(commands[0], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  for command in commands[1:]:
    ps_new = subprocess.Popen(command, stdin=ps.stdout,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ps.stdout.close()
    ps.stderr.close()
    ps.wait()
    ps = ps_new

  result = ps.stdout.readlines()
  ps.stdout.close()
  ps.stderr.close()
  ps.wait()
  return result

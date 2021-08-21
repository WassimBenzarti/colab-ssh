import pathlib


def add_to_authorized_keys(pub_ssh_keys):
  """
    pub_ssh_keys is a string that must have public keys
      seperated with new lines
  """

  ssh_folder_path = pathlib.Path(
      pathlib.Path.home(), ".ssh")
  # Make sure the .ssh folder exists
  ssh_folder_path.mkdir(
      parents=True, exist_ok=True)

  with open(ssh_folder_path.joinpath("authorized_keys"), "a") as f:
    f.write(pub_ssh_keys+"\n")

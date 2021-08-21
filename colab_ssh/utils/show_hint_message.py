
def _show_hint_title():
  print("Hint:")


def _tab_print(message):
  print("\t"+message)


def show_hint_message(unclear_message):
  output = ""
  if "could not read Username for 'https://" in unclear_message:
    output = "You probably have to enter your username and password"
  elif "Support for password authentication was removed" in unclear_message:
    output = "Support for password authentication was removed from github on August 13, 2021. Please use a personal access token instead (https://github.com/settings/tokens)."
  elif ("Invalid username or password" in unclear_message
        ) or (
      "HTTP Basic: Access denied"
  ):
    output = "Please check your username and password"

  if output:
    _show_hint_title()
    _tab_print(output)
  else:
    pass

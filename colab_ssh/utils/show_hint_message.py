
def _show_hint_title():
	print("Hint:")

def _tab_print(message):
	print("\t"+message)

def show_hint_message(unclear_message):
	output = ""
	if "could not read Username for 'https://github.com'" in unclear_message:
		output="You probably have to enter your username and password"
	elif "Invalid username or password" in unclear_message:
		output="Please check your username and password"
		pass

	if output:
		_show_hint_title()
		_tab_print(output)
	else:
		pass
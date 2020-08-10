
def _show_hint_title():
	print("Hint:")

def _tab_print(message):
	print("\t"+message)

def show_hint_message(unclear_message):
	
	if "could not read Username for 'https://github.com'" in unclear_message:
		_tab_print("You probably have to enter your username and password")
	else:
		pass
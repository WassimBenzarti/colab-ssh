from urllib.parse import quote


def ask_user_pass(username):
    username_input = input("Enter your username: {}\n".format(
        "(leave it empty if it's '{username}')" if username is not None else ""
    ))
    username = quote(username_input or username)
    # Get password
    from getpass import getpass
    password = quote(getpass('Enter your password: \n'))

    return username, password

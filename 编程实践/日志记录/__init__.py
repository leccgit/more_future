# This is our super secret key:
SECRET = 'this-is-a-secret'


class Error:
    def __init__(self):
        pass


# A malicious user can craft a format string that
# can read data from the global namespace:
user_input = '{error.__init__.__globals__[SECRET]}'

# This allows them to exfiltrate sensitive information,
# like the secret key:
err = Error()
print(user_input.format(error=err))

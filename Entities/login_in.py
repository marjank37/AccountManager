class Login:
    def __init__(self):
        self.valid_users = {
            "MARJAN": "1404",
            "user1": "pass1"
        }

    def validate(self, username, password):
        return self.valid_users.get(username.upper()) == password

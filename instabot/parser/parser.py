from .. import User, API


class Parser(API):

    def __init__(self):

        self.users = User.load_all()

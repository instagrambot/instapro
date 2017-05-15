import sys
from instabot.db_helper import DBHelper

is_py2 = sys.version[0] == '2'
if is_py2:
    from Queue import Queue
else:
    from queue import Queue

from .. import config

users_folder_path = config.PROJECT_FOLDER_PATH + config.USERS_FOLDER_NAME


class UserController(object):
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(UserController, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.queue = Queue()
        self.main_user = None

        self.db = DBHelper()

        self.load_all_users()

    @property
    def current(self):
        if not self.queue.empty():
            temp_user = self.queue.get()
            self.queue.put(temp_user)
            return temp_user

    @property
    def main(self):
        # todo проверка, что main_user задан
        return self.main_user

    @main.setter
    def main(self, user):
        self.main_user = user

    @main.deleter
    def main(self):
        del self.main_user

    def load_all_users(self):
        for user in self.db.get_all_users():
            self.queue.put(user)

    def load_user(self, name):
        return self.db.get_user(name)

    def save_user(self, user):
        self.db.insert_user(user)

    def delete_user(self, user):
        self.db.delete_user(user.name)

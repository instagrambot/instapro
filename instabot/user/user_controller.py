import os
import pickle
import random

from .. import config

users_folder_path = config.PROJECT_FOLDER_PATH + config.USERS_FOLDER_NAME


class UserController(object):
    def __init__(self):
        self.users = []
        self.current_user = None

    @classmethod
    def load_all_users(cls):
        users = []
        for user_path in os.listdir(users_folder_path):
            if user_path.endswith('.user'):
                username = user_path[:-5]
                users.append(cls.load_user(username))
        return filter(None, users)

    @classmethod
    def load_user(self, name):
        input_path = users_folder_path + "%s.user" % name
        if not os.path.exists(input_path):
            # warn
            return None

        with open(input_path, 'rb') as finput:
            try:
                return pickle.load(finput)
            except:
                #warnings.warn("%s is corrupted." % username)
                # warn
                os.remove(input_path)
                return None

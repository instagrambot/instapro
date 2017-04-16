import os
import pickle
import random

from instabot.new import config

users_folder_path = config.PROJECT_FOLDER_PATH + config.USERS_FOLDER_NAME


class UserController:
    def __init__(self):
        self.users = []
        self.current_user = None

    def load_all_users(self):
        for user_path in os.listdir(users_folder_path):
            if user_path.endswith('.user'):
                username = user_path[:-5]
                self.users.append(self.load(username))

    def load_user(self, name=None):
        if name is None:
            input_path = users_folder_path + \
                random.choice([x for x in os.listdir(
                    users_folder_path) if x.endswith('.user')])
        else:
            input_path = users_folder_path + "%s.user" % name
            if not os.path.exists(input_path):
                # warn
                return None

        with open(input_path, 'rb') as finput:
            try:
                self.current_user = pickle.load(finput)
            except:
                #warnings.warn("%s is corrupted." % username)
                # warn
                os.remove(input_path)
                return None

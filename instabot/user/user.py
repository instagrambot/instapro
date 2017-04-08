import os
import hmac
import pickle
import warnings
import json

from enum import IntEnum

from .. import config

users_folder_path = config.PROJECT_FOLDER_PATH + config.USERS_FOLDER_NAME

class Dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    __repr__ = dict.__repr__

    def __str__(self):
        s = ""
        for key, value in self.items():
            s += "%s: %s\n" % (str(key), str(value))
        return s

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)


class User(object):
    """ Class to store all user's properties """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.api_is_set = False
        self.bot_is_set = False
        self.isLoggedIn = False
        self.counters = Dotdict({})
        self.limits = Dotdict({})
        self.delays = Dotdict({})
        self.filters = Dotdict({})

    def save(self):
        if not os.path.exists(users_folder_path):
            if not os.path.exists(config.PROJECT_FOLDER_PATH):
                os.makedirs(config.PROJECT_FOLDER_PATH)
            os.makedirs(users_folder_path)
        output_path = users_folder_path + "%s.user" % self.username
        with open(output_path, 'wb') as foutput:
            pickle.dump(self, foutput)

    @classmethod
    def load(cls, username):
        """ returns the User class instance by username """
        input_path = users_folder_path + "%s.user" % username
        if os.path.exists(input_path):
            with open(input_path, 'rb') as finput:
                try:
                    dumped_user = pickle.load(finput)
                    return dumped_user
                except:
                    warnings.warn("%s is corrupted." % username)
                    cls.delete(username)
                    return None
        else:
            warnings.warn("No user found")
            return None

    @classmethod
    def load_all(cls):
        """ returns a list of all User instances """
        users = []
        for user_path in os.listdir(users_folder_path):
            if user_path[-5:] == ".user":
                username = user_path[:-5]
                users.append(User.load(username))
        return users

    @classmethod
    def get_all_users(cls):
        """ returns a list of usernames """
        if not os.path.exists(users_folder_path):
            return []
        return [path[:-5] for path in os.listdir(users_folder_path) if path[-5:] == ".user"]

    @staticmethod
    def delete(username):
        input_path = users_folder_path + "%s.user" % username
        if os.path.exists(input_path):
            os.remove(input_path)

    def dump(self):
        items = self.__dict__.copy()
        # del items["counters"]
        return json.dumps(items, indent=2)

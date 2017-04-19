import hashlib
import json
import os
import pickle
import uuid
import requests
import logging
from .. import config
from ..api.request import Request

users_folder_path = config.PROJECT_FOLDER_PATH + config.USERS_FOLDER_NAME


class Dotdict(dict):
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
    def __init__(self, username, password):
        self.name = username
        self.password = password
        self.device_uuid = str(uuid.uuid4())
        self.guid = str(uuid.uuid4())
        self.device_id = 'android-' + \
            hashlib.md5(username.encode('utf-8')).hexdigest()[:16]
        self.session = requests.Session()
        self.id = None
        self.logged_id = False
        self.counters = Dotdict({})
        self.limits = Dotdict({})
        self.delays = Dotdict({})
        self.filters = Dotdict({})

        if not self.login():
            return None

    def login(self):
        self.session.headers.update({
            'Connection': 'close',
            'Accept': '*/*',
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie2': '$Version=1',
            'Accept-Language': 'en-US',
            'User-Agent': config.USER_AGENT})

        data = {
            'phone_id': self.device_uuid,
            'username': self.name,
            'guid': self.guid,
            'device_id': self.device_id,
            'password': self.password,
            'login_attempt_count': '0'}

        message = Request.send(
            self.session, 'accounts/login/', json.dumps(data))
        if message is None:
            logging.getLogger('main').warning(self.name + ' login failed')
            self.logged_in = False
            self.save()
            return False
        self.id = str(message["logged_in_user"]["pk"])
        self.rank_token = "%s_%s" % (self.id, self.guid)
        self.logged_in = True
        logging.getLogger('main').info(self.name + ' successful authorization')
        self.save()
        return True

    def save(self):
        if not os.path.exists(users_folder_path):
            if not os.path.exists(config.PROJECT_FOLDER_PATH):
                os.makedirs(config.PROJECT_FOLDER_PATH)
            os.makedirs(users_folder_path)
        output_path = users_folder_path + "%s.user" % self.name
        with open(output_path, 'wb') as foutput:
            pickle.dump(self, foutput)

    def delete(self):
        input_path = users_folder_path + "%s.user" % self.name
        if os.path.exists(input_path):
            os.remove(input_path)

    def dump(self):
        items = self.__dict__.copy()
        # del items["counters"]
        return json.dumps(items, indent=2)

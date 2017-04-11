import uuid
import hashlib
import requests
import json
from instabot.new import Api
from instabot.new import Config


class User:
    def __init__(self, username, password):
        self.name = username
        self.password = password
        self.device_uuid = str(uuid.uuid4())
        self.guid = str(uuid.uuid4())
        self.device_id = 'android-' + hashlib.md5(username.encode('utf-8')).hexdigest()[:16]
        self.session = requests.Session()
        self.login()

    def login(self):
        self.session.headers.update({
            'Connection': 'close',
            'Accept': '*/*',
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie2': '$Version=1',
            'Accept-Language': 'en-US',
            'User-Agent': Config.USER_AGENT})

        data = {
            'phone_id': self.device_uuid,
            'username': self.name,
            'guid': self.guid,
            'device_id': self.device_id,
            'password': self.password,
            'login_attempt_count': '0'}

        message = Api.send_request(self.session, 'accounts/login/', Api.generate_signature(json.dumps(data)))

        self.id = str(message["logged_in_user"]["pk"])
        print('Success')

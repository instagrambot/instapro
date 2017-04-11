import uuid
import hashlib


class User:
    def __init__(self, username, password):
        self.name = username
        self.password = password
        self.device_uuid = str(uuid.uuid4())
        self.guid = str(uuid.uuid4())
        self.device_id = 'android-' + hashlib.md5(username.encode('utf-8')).hexdigest()[:16]
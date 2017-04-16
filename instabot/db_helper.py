import sqlite3
import pickle
from . import config
from .user.user_db import User

users_folder_path = config.PROJECT_FOLDER_PATH + config.USERS_FOLDER_NAME


class DBHelper(object):
    def __init__(self):
        self.conn = sqlite3.connect(users_folder_path + 'instabot.db')
        self.cursor = self.conn.cursor()
        create_table_query = '''CREATE TABLE IF NOT EXISTS accounts (
                                        name text NOT NULL UNIQUE,
                                        password text NOT NULL,
                                        user_id bigint NOT NULL,
                                        device_uuid text NOT NULL,
                                        guid text NOT NULL,
                                        device_id text NOT NULL,
                                        session text NOT NULL,
                                        counters text,
                                        limits text,
                                        delays text,
                                        filters text,
                                        PRIMARY KEY (user_id)
                                    );'''
        self.cursor.execute(create_table_query)

    def insert_user(self, user):
        try:
            user_data = (user.name, user.password, int(user.id), user.device_uuid, user.guid, user.device_id,
                         pickle.dumps(user.session), None, None, None, None)
            self.cursor.execute(
                'INSERT INTO accounts '
                'VALUES (?,?,?,?,?,?,?,?,?,?,?);', user_data)
        except sqlite3.DatabaseError as err:
            print("Error: ", err)
        else:
            self.conn.commit()

    def delete_user(self, username):
        try:
            self.cursor.execute(
                'DELETE FROM accounts '
                'WHERE name=(?);', (username,))
        except sqlite3.DatabaseError as err:
            print("Error: ", err)
        else:
            self.conn.commit()

    def get_user(self, name):
        self.cursor.execute('SELECT * FROM accounts '
                            'WHERE name=(?);', (name,))
        d = self.cursor.fetchone()
        return User(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9], d[10])

    def get_all_users(self):
        users = []
        for d in self.cursor.execute('SELECT * from accounts;'):
            users.append(User(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9], d[10]))
        return users
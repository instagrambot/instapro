from instabot import User, api, Parser
import logging.config
import unittest
from instabot.user.user_controller import UserController


test_login, test_password = 'instabotproject', 'drcherryisagoodman'

class TestUser(unittest.TestCase):

    # def test_user(self):
    #     user = User(test_login, test_password)
    #     print(api.get_user_followers(user, user.id))

    def test_parser(self):
        prs = Parser()
        resp = list(prs.user_followers(352300017, total=10))
        print (resp)
        self.assertEqual(len(resp), 10)



if __name__ == '__main__':

    user1 = User('login', 'pass')

    parser = Parser()
    print(list(parser.user_followers(user1.id, total=3)))



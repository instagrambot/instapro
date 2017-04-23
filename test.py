from instabot import User, api, Sender, Getter
import logging.config
import unittest
from instabot.user.user_controller import UserController


class TestUser(unittest.TestCase):

    def test_getter(self):
        get = Getter()
        print ("USERS AVAILABLE: %d" % get.controller.queue.qsize())
        resp = list(get.user_followers("4456846295"))
        self.assertTrue(len(resp) > 0)
        resp = list(get.user_following("4456846295", total=5))
        self.assertEqual(len(resp), 5)
        resp = list(get.user_feed("4456846295", total=10))
        self.assertEqual(len(resp), 10)

        resp = get.user_info("4456846295")
        self.assertEqual(resp["pk"], 4456846295)
        resp = get.user_info("ohld")
        self.assertEqual(resp["pk"], 352300017)

        resp = list(get.liked_media(total=0))
        self.assertEqual(len(resp), 0)

    def test_sender(self):
        send = Sender("instabotproject")
        self.assertTrue(send.can_follow("ohld"))
        self.assertFalse(send.follow_followers("ohld", total=1))

def add_users():
    pass

if __name__ == '__main__':
    logging.config.fileConfig('instabot/log.conf')
    log = logging.getLogger('main')
    # add_users()
    unittest.main()

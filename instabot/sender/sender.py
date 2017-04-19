from ..api.request import Request
from ..getter import Getter
from ..user.user_controller import UserController
import time
import json


class Sender(object):

    def __init__(self):
        self.controller = UserController()
        self.get = Getter()

    def can_follow(self):
        # check filter
        # check limit
        # check counters
        return True

    def follow_followers(self, main_target):
        if not str(main_target).isdigit():
            main_target = self.get.user_info(main_target)['pk']
        for target in self.get.user_followers(main_target):
            self.follow(target)
            time.sleep(1) # sleep for user.delay

    def follow(self, user_id):
        if self.can_follow():
            print('follow ' + user_id)
            return Request.send(self.controller.main.session, 'friendships/create/' + str(user_id) + '/', '{}')

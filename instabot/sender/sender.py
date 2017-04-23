import time
import json
import warnings


from ..api.request import Request
from ..getter import Getter
from ..user import UserController, User


class Sender(object):

    def __init__(self, username, password=None):
        self.get = Getter()
        self.controller = self.get.controller  # for shortage
        if password is not None:
            user = User(username, password)
            if user is not None:
                self.controller.main = user
            else:
                return None
        else:
            self.controller.main = self.controller.load_user(username)
        self.main = self.controller.main  # for shortage

    def can_follow(self, usr=None):
        # check filter
        # check limit
        # check counters
        if usr is not None and isinstance(usr, dict):
            if not hasattr(self.main, "following"):
                self.main.following = set(
                    [usr["pk"] for usr in self.get.user_following(self.main.id)])
            if usr["pk"] in self.main.following:
                return False
            if "is_business" in usr and usr["is_business"]:
                return False
            if "is_verified" in usr and usr["is_verified"]:
                return False

        return True

    def can_like(self, target=None):
        # check filter
        # check limit
        # check counters
        return True

    def follow_followers(self, main_target, total=None):
        if not str(main_target).isdigit():
            main_target = self.get.user_info(main_target)['pk']
        return self.follow_users(self.get.user_followers(main_target, total=total))

    def follow_following(self, main_target):
        if not str(main_target).isdigit():
            main_target = self.get.user_info(main_target)['pk']
        return self.follow_users(self.get.user_following(main_target, total=total))

    def follow_users(self, targets):
        for target in targets:
            if self.follow(target) is None:
                warnings.warn("Error while following %s." % target["username"])
            time.sleep(10)  # sleep for user.delay
        return False  # exitcode 0 - no errors

    def follow(self, target):
        if self.can_follow(target):
            print(target['username'] + 'was followed.')
            return Request.send(self.controller.main.session, 'friendships/create/' + str(target['pk']) + '/', '{}')

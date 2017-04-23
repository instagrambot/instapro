import time
import json
import warnings

from random import random

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

    def can_like(self, md=None):
        # check filter
        # check limit
        # check counters
        if md is not None:
            if "has_liked" in md and md["has_liked"]:
                return False
        return True

    def follow_followers(self, main_target, total=None):
        if not str(main_target).isdigit():
            main_target = self.get.user_info(main_target)['pk']
        return self.follow_users(self.get.user_followers(main_target, total=total))

    def follow_following(self, main_target, total=None):
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
            print("follow %s" % target['username'])
            return Request.send(self.controller.main.session, 'friendships/create/' + str(target['pk']) + '/', '{}')
        return False

    def like(self, media):
        if self.can_like(media):
            print("like %s's media" % media['user']['username'])
            return Request.send(self.controller.main.session, 'media/' + str(media['pk']) + '/like/', '{}')
        return False

    def like_medias(self, medias):
        for media in medias:
            if self.like(media) is None:
                warnings.warn("Error while liking %s's media." %
                              media['user']['pk'])
        return False  # exitcode 0 - no errors

    def like_geo_medias(self, location, total=None):
        if not str(location).isdigit():
            location = self.get.geo_id(location)
        return self.like_medias(self.get.geo_medias(location, total=total))

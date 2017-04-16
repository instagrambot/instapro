import time
import warnings
from queue import Queue
from tqdm import tqdm

from instabot.api import api
from instabot.user.user_controller import UserController


class Getter(object):

    def __init__(self):
        self.controller = UserController()

    def user_getter(func):
        def debug_wrapper(*args, **kwargs):
            self = args[0]
            while True:
                user = self.controller.get_user
                kwargs['user'] = user
                try:
                    res = func(*args, **kwargs)
                    return res
                except Exception as e:
                    warnings.warn("GETTER:", str(e))
                    time.sleep(5)
                    continue
        return debug_wrapper

    def error_handler(func):
        def error_handler_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                warnings.warn('GETTER: ' + str(e))
                time.sleep(2)
        return error_handler_wrapper

    @error_handler
    @user_getter
    def _get_user_followers(self, user_id, max_id='', user=None):
        if user is None:
            raise Exception("No User instance was passed")
        resp = api.get_user_followers(user, user_id, maxid=max_id)
        if resp is None:
            raise Exception("Broken User: %s" % user.name)
        if not resp['big_list']:
            return (resp['users'], None)
        return (resp['users'], resp['next_max_id'])

    # @error_handler
    # @api_getter
    # def _get_user_following(self, user_id, max_id="", api=None):
    #     if api is None:
    #         raise ("No API instance was passed")
    #     if not api.getUserFollowings(user_id, maxid=max_id):
    #         raise ("Broken API")
    #     if not api.LastJson["big_list"]:
    #         return (api.LastJson["users"], None)
    #     return (api.LastJson["users"], api.LastJson["next_max_id"])
    #
    # @error_handler
    # @api_getter
    # def _get_user_info(self, user_id, api=None):
    #     if api is None:
    #         raise ("No API instance was passed")
    #     if not api.getUsernameInfo(user_id):
    #         raise ("Broken API")
    #     if "user" in api.LastJson:
    #         return api.LastJson["user"]
    #     return None

    @error_handler
    @user_getter
    def _get_user_feed(self, user_id, max_id="", user=None):
        if user is None:
            raise Exception("No User instance was passed")
        resp = api.get_user_feed(user, user_id, maxid=max_id)
        if resp is None:
            raise Exception("Broken User: %s" % user.name)
        if "next_max_id" not in resp or "more_available" in resp and not resp["more_available"]:
            return (resp["items"], None)
        return (resp["items"], resp["next_max_id"])

    # @error_handler
    # @api_getter
    # def _get_liked_media(self, max_id="", api=None):
    #     if api is None:
    #         raise ("No API instance was passed")
    #     if not api.getLikedMedia(max_id):
    #         raise ("Broken API")
    #     if not api.LastJson["more_available"]:
    #         return (["items"], None)
    #     return (api.LastJson["items"], api.LastJson["next_max_id"])

    @staticmethod
    def generator(func, arg, total=None):
        max_id = ""
        count = 0
        while True:
            if arg is not None:
                resp = func(arg, max_id=max_id)
            else:
                resp = func(max_id)
            if resp is None:
                time.sleep(2)
                continue
            items, max_id = resp
            for item in items:
                count += 1
                if total is not None and total < count:
                    break
                yield item
            if max_id is None or total is not None and total < count:
                break

    # def get_user_info(self, user_id):
    #     return self._get_user_info(user_id)

    def user_followers(self, user_id, total=None):
        """ generator to iterate over user's followers """
        return self.generator(self._get_user_followers, user_id, total=total)

    # def user_following(self, user_id, total=None):
    #     """ generator to iterate over user's following """
    #     return self.generator(self._get_user_following, user_id, total)

    def user_feed(self, user_id, total=None):
        """ generator to iterate over user feed """
        return self.generator(self._get_user_feed, user_id, total=total)
    #
    # def liked_media(self, total=None):
    #     """ generator to iterate over liked medias """
    #     return self.generator(self._get_liked_media, None, total)

import time
import warnings
import sys
from random import random
from tqdm import tqdm

is_py2 = sys.version[0] == '2'
if is_py2:
    from Queue import Queue
else:
    from queue import Queue
from instabot.api import api
from instabot.user.user_controller import UserController


class Getter(object):
    def __init__(self):
        self.controller = UserController()

    def error_handler(func):
        def error_handler_wrapper(*args, **kwargs):
            self = args[0]
            while True:
                kwargs['user'] = self.controller.user
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    warnings.warn('GETTER: ' + str(e))
                    time.sleep(60 * random())
                    continue

        return error_handler_wrapper

    @error_handler
    def _get_user_followers(self, user_id, max_id='', user=None):
        if user is None:
            raise Exception("No User instance was passed")
        resp = api.get_user_followers(user, user_id, maxid=max_id)
        if resp is None:
            raise Exception("Broken User: %s" % user.name)
        if "next_max_id" not in resp or "big_list" in resp and not resp['big_list']:
            return (resp['users'], None)
        return (resp['users'], resp['next_max_id'])

    @error_handler
    def _get_user_following(self, user_id, max_id="", user=None):
        if user is None:
            raise Exception("No User instance was passed")
        resp = api.get_user_following(user, user_id, maxid=max_id)
        if resp is None:
            raise Exception("Broken User")
        if "next_max_id" not in resp or "big_list" in resp and not resp["big_list"]:
            return (resp["users"], None)
        return (resp["users"], resp["next_max_id"])

    @error_handler
    def _get_user_info(self, user_id, user=None):
        if user is None:
            raise Exception("No User instance was passed")
        resp = api.get_user_info(user, user_id)
        if resp is None:
            raise Exception("Broken User")
        if "user" in resp:
            return resp["user"]
        return None

    @error_handler
    def _get_geo_id(self, location_name, user=None):
        if user is None:
            raise Exception("No User instance was passed")
        resp = api.search_location(user, location_name)
        if resp is None:
            raise Exception("Broken User")
        try:
            return resp["items"][0]['location']['pk']
        except:
            return None

    @error_handler
    def _get_user_feed(self, user_id, max_id="", user=None):
        if user is None:
            raise Exception("No User instance was passed")
        resp = api.get_user_feed(user, user_id, maxid=max_id)
        if resp is None:
            # just user is private
            return ([], None)
        if "next_max_id" not in resp or "more_available" in resp and not resp["more_available"]:
            return (resp["items"], None)
        return (resp["items"], resp["next_max_id"])

    @error_handler
    def _get_liked_media(self, max_id="", user=None):
        if user is None:
            raise Exception("No API instance was passed")
        resp = api.get_liked_media(user, max_id)
        if resp is None:
            raise Exception("Broken API")
        if "next_max_id" not in resp or "more_available" in resp and not resp["more_available"]:
            return (resp["items"], None)
        return (resp["items"], resp["next_max_id"])

    @error_handler
    def _get_geo_medias(self, location_id, max_id="", user=None):
        if user is None:
            raise Exception("No API instance was passed")
        resp = api.get_geo_feed(user, location_id, max_id)
        if resp is None:
            raise Exception("Broken API")
        if "next_max_id" not in resp or "more_available" in resp and not resp["more_available"]:
            return (resp["items"], None)
        return (resp["items"], resp["next_max_id"])

    @error_handler
    def _get_hashtag_medias(self, hashtag, max_id="", user=None):
        if user is None:
            raise Exception("No API instance was passed")
        resp = api.get_hashtag_feed(user, hashtag, max_id)
        if resp is None:
            raise Exception("Broken API")
        if "next_max_id" not in resp or "more_available" in resp and not resp["more_available"]:
            return (resp["items"], None)
        return (resp["items"], resp["next_max_id"])

    @staticmethod
    def generator(func, arg, total=None):
        max_id = ""
        count = 0
        while True:
            time.sleep(0.5 * random())
            if max_id is None or total is not None and total < count:
                break
            if arg is not None:
                resp = func(arg, max_id=max_id)
            else:
                resp = func(max_id=max_id)
            if resp is None:
                time.sleep(5 * random())
                continue
            items, max_id = resp
            for item in items:
                count += 1
                if total is not None and total < count:
                    break
                yield item

    def user_info(self, user_id):
        """ returns dict with user's info. You can pass as username as user_id. """
        time.sleep(0.5 * random())
        return self._get_user_info(user_id)

    def user_followers(self, user_id, total=None):
        """ generator to iterate over user's followers """
        return self.generator(self._get_user_followers, user_id, total=total)

    def user_following(self, user_id, total=None):
        """ generator to iterate over user's following """
        return self.generator(self._get_user_following, user_id, total=total)

    def user_feed(self, user_id, total=None):
        """ generator to iterate over user feed """
        return self.generator(self._get_user_feed, user_id, total=total)

    # TODO: make this method iterate over main user's liked media
    # def liked_media(self, total=None):
    #     """ generator to iterate over liked medias """
    #     return self.generator(self._get_liked_media, None, total=total)

    def geo_medias(self, location_id, total=None):
        """ generator to iterate over geo medias """
        return self.generator(self._get_geo_medias, location_id, total=total)

    def hashtag_medias(self, hashtag, total=None):
        """ generator to iterate over hashtag medias """
        return self.generator(self._get_hashtag_medias, hashtag, total=total)

    def geo_id(self, location_name):
        return self._get_geo_id(location_name)

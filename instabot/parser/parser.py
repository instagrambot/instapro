import time
import warnings
from queue import Queue
from tqdm import tqdm

from .. import User, API


class Parser(object):

    def __init__(self, apis=None):
        if apis is None:
            self.apis = API.load_all()
        else:
            self.apis = apis
        if apis is None or len(apis) == 0:
            warnings.warn("PARSER: No API found.")
            return None

        self.queue = Queue()
        for api in self.apis:
            self.queue.put(api)

    def api_getter(func):
        def debug_wrapper(*args, **kwargs):
            self = args[0]
            if not self.queue.empty():
                api = self.queue.get()
                kwargs['api'] = api
                res = func(*args, **kwargs)
                self.queue.put(api)
                return res
            return None
        return debug_wrapper

    def error_handler(func):
        def error_handler_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                warnings.warn("PARSER: " + str(e))
                time.sleep(2)
        return error_handler_wrapper

    @error_handler
    @api_getter
    def _get_user_followers(self, user_id, max_id="", api=None):
        if api is None:
            raise ("No API instance was passed")
        if not api.getUserFollowers(user_id, maxid=max_id):
            raise ("Broken API")
        if not api.LastJson["big_list"]:
            return (api.LastJson["users"], None)
        return (api.LastJson["users"], api.LastJson["next_max_id"])

    @error_handler
    @api_getter
    def _get_user_following(self, user_id, max_id="", api=None):
        if api is None:
            raise ("No API instance was passed")
        if not api.getUserFollowings(user_id, maxid=max_id):
            raise ("Broken API")
        if not api.LastJson["big_list"]:
            return (api.LastJson["users"], None)
        return (api.LastJson["users"], api.LastJson["next_max_id"])

    @error_handler
    @api_getter
    def _get_user_info(self, user_id, api=None):
        if api is None:
            raise ("No API instance was passed")
        if not api.getUsernameInfo(user_id):
            raise ("Broken API")
        if "user" in api.LastJson:
            return api.LastJson["user"]
        return None

    @error_handler
    @api_getter
    def _get_user_feed(self, user_id, max_id="", api=None):
        if api is None:
            raise ("No API instance was passed")
        if not api.getUserFeed(user_id, maxid=max_id):
            raise ("Broken API")
        if not api.LastJson["more_available"]:
            return (api.LastJson["items"], None)
        return (api.LastJson["items"], api.LastJson["next_max_id"])

    @error_handler
    @api_getter
    def _get_liked_media(self, max_id="", api=None):
        if api is None:
            raise ("No API instance was passed")
        if not api.getLikedMedia(max_id):
            raise ("Broken API")
        if not api.LastJson["more_available"]:
            return (["items"], None)
        return (api.LastJson["items"], api.LastJson["next_max_id"])

    @staticmethod
    def generator(func, arg, total=None):
        max_id = ""
        count = 0
        while True:
            if arg is not None:
                resp = func(arg, max_id)
            else:
                resp = func(max_id)
            if resp is None:
                time.sleep(2)
                continue
            items, max_id = resp
            for item in items:
                count += 1
                yield item
            if max_id is None:
                break
            if total is not None and total <= count:
                break

    def get_user_info(self, user_id):
        return self._get_user_info(user_id)

    def user_followers(self, user_id, total=None):
        """ generator to iterate over user's followers """
        return self.generator(self._get_user_followers, user_id, total)

    def user_following(self, user_id, total=None):
        """ generator to iterate over user's following """
        return self.generator(self._get_user_following, user_id, total)

    def user_feed(self, user_id, total=None):
        """ generator to iterate over user feed """
        return self.generator(self._get_user_feed, user_id, total)

    def liked_media(self, total=None):
        """ generator to iterate over liked medias """
        return self.generator(self._get_liked_media, None, total)

    def get_user_followers(self, user_id):
        result = []
        max_id = ""
        user_info = self._get_user_info(user_id)
        if user_info is None:
            return []

        total_followers = user_info["follower_count"]
        with tqdm(total=total_followers, desc="Getting followers", leave=False) as pbar:
            while True:
                resp = self._get_user_followers(user_id, max_id)
                if resp is None:
                    continue
                users, max_id = resp

                pbar.update(len(users))
                result.extend(users)

                if max_id is None:
                    break
        result = result[:total_followers]
        return result

    def get_user_following(self, user_id):
        result = []
        max_id = ""
        user_info = self._get_user_info(user_id)
        if user_info is None:
            return []

        total_following = user_info["follower_count"]
        with tqdm(total=total_following, desc="Getting followers", leave=False) as pbar:
            while True:
                resp = self._get_user_following(user_id, max_id)
                if resp is None:
                    continue
                users, max_id = resp

                pbar.update(len(users))
                result.extend(users)

                if max_id is None:
                    break
        result = result[:total_following]
        return result

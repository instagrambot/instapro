import time
import warnings
from Queue import Queue
from tqdm import tqdm

from .. import User, API


class Parser(object):

    def __init__(self):
        self.apis = API.load_all()
        self.queue = Queue()
        for api in self.apis:
            self.queue.put(api)

    def api_getter(func):
        def debug_wrapper(*args, **kwargs):
            self = args[0]
            if not self.queue.empty():
                api = self.queue.get()
                kwargs['api'] = api
                result = func(*args, **kwargs)
                self.queue.put(api)
                return result
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
        result = api.LastJson
        if result["big_list"] is False:
            return (result["users"], None)

        next_max_id = result["next_max_id"]
        return (result["users"], next_max_id)

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

    def get_user_info(self, user_id):
        return self._get_user_info(user_id)

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
        # assert(len(result) == len(set(result)))
        return result



    # def get_total_followers(self, user_id):
    #
    #
    #
    #     followers = []
    #     next_max_id = ''
    #     self.getUsernameInfo(usernameId)
    #     if "user" in self.LastJson:
    #         total_followers = self.LastJson["user"]['follower_count']
    #     else:
    #         return False
    #     with tqdm(total=total_followers, desc="Getting followers", leave=False) as pbar:
    #         while True:
    #             self.getUserFollowers(usernameId, next_max_id)
    #             temp = self.LastJson
    #             try:
    #                 pbar.update(len(temp["users"]))
    #                 for item in temp["users"]:
    #                     followers.append(item)
    #                 if len(temp["users"]) == 0 or len(followers) >= total_followers:
    #                     return followers[:total_followers]
    #             except:
    #                 return followers[:total_followers]
    #             if temp["big_list"] is False:
    #                 return followers[:total_followers]
    #             next_max_id = temp["next_max_id"]

from Queue import Queue

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

    @api_getter
    def get_user_followers(self, user_id, max_id="", api=None):
        if api == None:
            assert(not "No api.")
        api.getUserFollowers(user_id, maxid=max_id)
        result = api.LastJson
        users = result["users"]
        if result["big_list"] is False:
            return (users, None)

        next_max_id = result["next_max_id"]
        return (users, next_max_id)


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

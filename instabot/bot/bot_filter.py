"""
    Filter functions for media and user lists.

    Userlist workflow:

        -- You get a list from any getter (from hashtag / user's followers etc.)
        -- You pass it throw self.prefilter_users()
        --

"""

from tqdm import tqdm

from . import delay

# filtering medias


def filter_medias(self, media_items, filtration=True):
    if filtration:
        self.logger.info("Recieved %d medias." % len(media_items))
        media_items = _filter_medias_not_liked(media_items)
        if self.User.limits.max_likes_to_like:
            media_items = _filter_medias_nlikes(
                media_items, self.User.limits.max_likes_to_like)
        self.logger.info("After filtration %d medias left." % len(media_items))
    return _get_media_ids(media_items)


def _filter_medias_not_liked(media_items):
    not_liked_medias = []
    for media in media_items:
        if 'has_liked' in media.keys():
            if not media['has_liked']:
                not_liked_medias.append(media)
    return not_liked_medias


def _filter_medias_nlikes(media_items, max_likes_to_like):
    filtered_medias = []
    for media in media_items:
        if 'like_count' in media.keys():
            if media['like_count'] < max_likes_to_like:
                filtered_medias.append(media)
    return filtered_medias


def _get_media_ids(media_items):
    result = []
    for m in media_items:
        if 'pk' in m.keys():
            result.append(m['pk'])
    return result


def check_media(self, media_id):
    self.mediaInfo(media_id)
    if len(self.filter_medias(self.LastJson["items"])):
        return check_user(self, self.get_media_owner(media_id))
    else:
        return False

#################################################
#################################################


def search_stop_words_in_user(self, user_info):
    text = ''
    if 'biography' in user_info:
        text += user_info['biography'].lower()

    if 'username' in user_info:
        text += user_info['username'].lower()

    if 'full_name' in user_info:
        text += user_info['full_name'].lower()

    for stop_word in self.User.filters.stop_words:
        if stop_word in text:
            return True

    return False


def prefilter_users_to_follow(self, user_ids):
    """ Drops users from whitelist and blacklist and already followed
        Also converts all items in user_ids from username to user_id.
    """
    filtered = []
    for user_id in tqdm(user_ids, desc="Prefiltering users to follow", leave=False):
        user_id = self.convert_to_user_id(user_id)
        if not user_id:
            continue
        if self.User.blacklist and user_id in self.User.blacklist:
            continue
        if self.User.whitelist and user_id in self.User.whitelist:
            continue
        if user_id in self.User.following:
            continue
        filtered.append(user_id)
    if len(filtered) == len(user_ids):
        self.logger.debug("Nothing was filtered in prefilter to follow")
    return filtered


def prefilter_users_to_unfollow(self, user_ids):
    """ Drops users from whitelist and not followed
        Also converts all items in user_ids from username to user_id.
    """
    filtered = []
    for user_id in tqdm(user_ids, desc="Prefiltering users to unfollow", leave=False):
        user_id = self.convert_to_user_id(user_id)
        if not user_id:
            continue
        if user_id not in self.User.following:
            continue  # don't follow the current user
        if self.User.whitelist and user_id in self.User.whitelist:
            continue  # whitelist - users not to unfollow
        filtered.append(user_id)
    return filtered


def prefilter_users_to_interract(self, user_ids):
    """ Drops users from blacklist
        Also converts all items in user_ids from username to user_id.
    """
    filtered = []
    for user_id in tqdm(user_ids, desc="Prefiltering users to interract", leave=False):
        user_id = self.convert_to_user_id(user_id)
        if not user_id:
            continue
        if self.User.blacklist and user_id in self.User.blacklist:
            continue  # blacklist - users not to interract
        filtered.append(user_id)
    return filtered


def filter_users(self, user_id_list):
    return [int(user["pk"]) for user in user_id_list]


def check_user(self, user_id, filter_closed_acc=False):
    if not self.User.filters.filter_users:
        return True

    delay.small_delay(self)
    user_id = self.convert_to_user_id(user_id)

    user_info = self.get_user_info(user_id)
    if not user_info:
        return False
    if filter_closed_acc and "is_private" in user_info:
        if user_info["is_private"]:
            return False
    if "is_business" in user_info:
        if user_info["is_business"]:
            return False
    if "is_verified" in user_info:
        if user_info["is_verified"]:
            return False
    if "follower_count" in user_info and "following_count" in user_info:
        if user_info["follower_count"] < self.User.filters.min_followers_to_follow:
            return False
        if user_info["follower_count"] > self.User.filters.max_followers_to_follow:
            return False
        if user_info["following_count"] < self.User.filters.min_following_to_follow:
            return False
        if user_info["following_count"] > self.User.filters.max_following_to_follow:
            return False
        try:
            if user_info["follower_count"] / user_info["following_count"] \
                    > self.User.filters.max_followers_to_following_ratio:
                return False
            if user_info["following_count"] / user_info["follower_count"] \
                    > self.User.filters.max_following_to_followers_ratio:
                return False
        except ZeroDivisionError:
            return False

    if 'media_count' in user_info:
        if user_info["media_count"] < self.User.filters.min_media_count_to_follow:
            return False  # bot or inactive user

    if search_stop_words_in_user(self, user_info):
        return False

    return True


def check_not_bot(self, user_id):
    delay.small_delay(self)
    """ Filter bot from real users. """
    user_id = self.convert_to_user_id(user_id)
    if not user_id:
        return False
    if self.User.whitelist and user_id in self.User.whitelist:
        return True
    if self.User.blacklist and user_id in self.User.blacklist:
        return False

    user_info = self.get_user_info(user_id)
    if not user_info:
        return True  # closed acc

    if "following_count" in user_info:
        if user_info["following_count"] > self.User.filters.max_following_to_block:
            return False  # massfollower

    if search_stop_words_in_user(self, user_info):
        return False

    return True

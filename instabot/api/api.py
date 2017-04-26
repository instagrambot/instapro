from instabot.api.request import Request


def is_id(smth):
    ''' checks if input string is a number '''
    if str(smth).isdigit():
        return True
    return False


def get_user_info(user, user_id):
    if is_id(user_id):
        return Request.send(user.session,
                            'users/' + str(user_id) + '/info/')
    else:  # username was passed
        return Request.send(user.session,
                            'users/' + str(user_id) + '/usernameinfo/')


def get_user_feed(user, user_id, maxid='', minTimestamp=None):
    return Request.send(user.session,
                        'feed/user/' + str(user_id) + '/?max_id=' + str(maxid) + '&min_timestamp=' + str(minTimestamp) +
                        '&rank_token=' + str(user.rank_token) + '&ranked_content=true')


def get_user_followers(user, user_id, maxid=''):
    return Request.send(user.session,
                        'friendships/' + str(user_id) + '/followers/?max_id=' + str(maxid) + '&rank_token=' + user.rank_token)


def get_user_following(user, user_id, maxid=''):
    return Request.send(user.session,
                        'friendships/' + str(user_id) + '/following/?max_id=' + str(maxid) + '&rank_token=' + str(user.rank_token))


def get_liked_media(user, maxid=''):
    return Request.send(user.session,
                        'feed/liked/?max_id=' + str(maxid))


def search_location(user, query):
    return Request.send(user.session,
                        'fbsearch/places/?rank_token=' + str(user.rank_token) + '&query=' + str(query))


def get_geo_feed(user, location_id, maxid=''):
    return Request.send(user.session,
                        'feed/location/' + str(location_id) + '/?max_id=' + str(maxid) + '&rank_token=' + user.rank_token + '&ranked_content=true&')


def get_hashtag_feed(user, hashtag, maxid=''):
    return Request.send(user.session,
                        'feed/tag/' + str(hashtag) + '/?max_id=' + str(maxid) + '&rank_token=' + user.rank_token + '&ranked_content=true&')

from instabot.new.api import request


def get_profile_data(user):
    return request.send(user.session, 'users/' + user.id + '/info/')


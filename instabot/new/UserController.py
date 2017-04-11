from instabot.new.User import User
from instabot.new import Api


def test_request(user):
    return Api.send_request(user.session, 'users/' + user.id + '/info/')

user = User('USERNAME', 'PASSWORD')
print(test_request(user))

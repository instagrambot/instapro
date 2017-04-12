from instabot.new.user.user import User
from instabot.new.user.user_controller import UserController
from instabot.new.api import api


user1 = User('mybusiness_1466018390', 'TdFfsrTf23');
user2 = User('mybusiness_1466020273', 'TdFfsrTf23');
#user3 = User('login', 'pass');

controller = UserController()

controller.load_user()
print(api.get_profile_data(controller.current_user))

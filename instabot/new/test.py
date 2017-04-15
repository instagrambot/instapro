from instabot.new.user.user import User
from instabot.new.user.user_controller import UserController
from instabot.new.api import api
import logging.config

logging.config.fileConfig('log.conf')
log = logging.getLogger('main')
log.info('Start!')

#user1 = User('log', 'pass');
#user2 = User('log', 'pass');
user3 = User('log', 'pass');

controller = UserController()

controller.load_user()
print(api.get_profile_data(controller.current_user))

import argparse
import sys
import time

sys.path.append('../../')
from instabot import User, Getter

import config  # config file from the same folder
import scraper

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('user', type=str, nargs='+',
                    help='user which followers you want to scrape')
args = parser.parse_args()

get = Getter()
print ("USERS AVAILABLE: %d" % get.controller.queue.qsize())

path = config.outputpath + "followers_%s.tsv"

for username in args.user:
    user_id = get.user_info(username)["pk"]
    iterator = get.user_followers(user_id)
    scraper.save_users_from_user(get, iterator, path % username, batchsleep=10)
    time.sleep(120)

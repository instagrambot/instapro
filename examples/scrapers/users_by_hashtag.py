import argparse
import sys
import time

sys.path.append('../../')
from instabot import User, Getter

import config  # config file from the same folder
import scraper

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('hashtag', type=str, nargs='+',
                    help='hashtag which authors you want to scrape')
args = parser.parse_args()

get = Getter()
print ("USERS AVAILABLE: %d" % get.controller.queue.qsize())

path = config.outputpath + "hashtag_%s.tsv"

for hashtag in args.hashtag:
    iterator = get.hashtag_medias(hashtag)
    scraper.save_users_from_media(get, iterator, path % hashtag, batchsleep=12)
    time.sleep(120)

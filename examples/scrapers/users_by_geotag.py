import argparse
import sys
import time

sys.path.append('../../')
from instabot import User, Getter

import config  # config file from the same folder
import scraper

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('geotag', type=str, nargs='+',
                    help='geotag which authors you want to scrape')
args = parser.parse_args()

get = Getter()
print ("USERS AVAILABLE: %d" % get.controller.queue.qsize())

path = config.outputpath + "geotag_%s.tsv"

for geotag in args.geotag:
    location_id = get.geo_id(geotag)

    iterator = get.geo_medias(location_id)
    scraper.save_users_from_media(get, iterator, path % geotag, batchsleep=10)
    time.sleep(120)

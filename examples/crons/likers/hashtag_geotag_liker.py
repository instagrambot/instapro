import sys
import time
from tqdm import tqdm

sys.path.append('../../../')
from instabot import User, Sender

main_username = "ohld" # this user should be logger to instapro earlier
send = Sender(main_username)

with open("hashtags.txt", "r") as f:
    hashtags = [x.strip() for x in f.readlines()]

with open("geotags.txt", "r") as f:
    locations = [x.strip() for x in f.readlines()]

for location in tqdm(locations, desc="locations"):
    send.like_geo_medias(location, total=10, delay=15)

time.sleep(10 * 60) # 10 minutes between locations and hashtags

for hashtag in tqdm(hashtags, desc="hashtags"):
    send.like_hashtag_medias(hashtag, total=10, delay=15)

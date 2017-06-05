import sys
import time
from random import random
from tqdm import tqdm

sys.path.append('../../../')
from instabot import User, Sender

main_username = "ohld" # this user should be logged to instapro earlier
send = Sender(main_username)

with open("hashtags.txt", "r", encoding='utf-8') as f:
    hashtags = [x.strip() for x in f.readlines()]

with open("geotags.txt", "r", encoding='utf-8') as f:
    locations = [x.strip() for x in f.readlines()]

time.sleep(random() * 1 * 60) # 1 minute sleep

for location in tqdm(locations, desc="locations"):
    send.like_geo_medias(location, total=10, delay=15)

time.sleep(random() * 10 * 60) # 10 minutes between locations and hashtags

for hashtag in tqdm(hashtags, desc="hashtags"):
    send.like_hashtag_medias(hashtag, total=10, delay=15)

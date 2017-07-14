"""
    Functions that are used in scrapper scripts.
    (should be moved to instapro core?)

    by: okhlopkov.com
"""

import sys
import os
import time
import gc
import pandas as pd
from tqdm import tqdm


def dump_data(users, output_filename):
    data = pd.DataFrame(users)
    mode = "w"
    if os.path.isfile(output_filename):
        mode = "a"
    data.to_csv(output_filename, mode=mode, sep="\t",
                header=(mode == "w"), index=False)


def filter_user_info(ud):
    bad_keys = ["hd_profile_pic_url_info", "hd_profile_pic_versions", "external_lynx_url",
                "profile_pic_id", "profile_pic_url", "pk"]
    for key in bad_keys:
        ud.pop(key, None)
    return ud


def read_usernames(output_filename):
    if os.path.isfile(output_filename):
        return set(pd.read_table(output_filename, usecols=["username"])["username"])
    return set()


def save_users_from_media(get, iterator, output_filename, batchsize=100, batchsleep=12):
    pbar = tqdm(desc="unique users")
    usernames = read_usernames(output_filename)
    pbar.update(len(usernames))

    i = 0
    users = []
    for media in tqdm(iterator, desc="total  users"):
        if media["user"]["username"] in usernames:
            continue

        i += 1
        usernames.add(media["user"]["username"])

        usr = {}
        usr["user_id"] = media["user"]["pk"]
        if media["user"]["is_private"]:
            usr["username"] = media["user"]["username"]
            usr["full_name"] = media["user"]["full_name"]
        else:
            user_info = get.user_info(usr["user_id"])
            usr.update(filter_user_info(user_info))

        users.append(usr)
        pbar.update(1)
        if i % batchsize == 0:
            dump_data(users, output_filename)
            users = []
            gc.collect()
            time.sleep(batchsleep)

    dump_data(users, output_filename)
    users = []
    pbar.close()


def save_users_from_user(get, iterator, output_filename, batchsize=100, batchsleep=12):
    pbar = tqdm(desc="unique users")
    usernames = read_usernames(output_filename)
    pbar.update(len(usernames))

    i = 0
    users = []
    for _user in tqdm(iterator, desc="total  users"):
        if _user["username"] in usernames:
            continue

        i += 1
        usernames.add(_user["username"])

        usr = {}
        usr["user_id"] = _user["pk"]
        if _user["is_private"]:
            usr["username"] = _user["username"]
            usr["full_name"] = _user["full_name"]
        else:
            user_info = get.user_info(usr["user_id"])
            usr.update(filter_user_info(user_info))

        users.append(usr)
        pbar.update(1)
        if i % batchsize == 0:
            dump_data(users, output_filename)
            users = []
            gc.collect()
            time.sleep(batchsleep)

    dump_data(users, output_filename)
    users = []
    pbar.close()

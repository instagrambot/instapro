import json
import time
import hashlib
import hmac
import logging
from instabot.new import config


def send(session, endpoint, post=None):
    log = logging.getLogger('main')

    try:
        if post is not None:  # POST
            response = session.post(config.API_URL + endpoint, data=generate_signature(post))
        else:  # GET
            response = session.get(config.API_URL + endpoint)
        if response.status_code == 200:
            log.debug("Request OK! Response: " + response.text)
            #print(response)
            return json.loads(response.text)
        else:
            log.error("Request return " + str(response.status_code) + " error!")
            print(response.text)
            if response.status_code == 429:
                sleep_minutes = 5
                log.warning("That means 'too many requests'. I'll go to sleep for %d minutes." % sleep_minutes)
                time.sleep(sleep_minutes * 60)
            return
    except Exception as e:
        print(str(e))
        return


def generate_signature(data):
    return 'ig_sig_key_version=' + config.SIG_KEY_VERSION + '&signed_body=' + hmac.new(
        config.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + '.' + data

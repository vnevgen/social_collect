__author__ = 'vitaly'

import time

from TwitterAPI import TwitterAPI as _TwitterAPI
from ..filesystem import cache_file

from django.conf import settings

def getTwitterAPI():
    t_api = _TwitterAPI(
            settings.TOKEN_TWITTER_CONSUMER_KEY,
            settings.TOKEN_TWITTER_CONSUMER_SECRET,
            settings.TOKEN_TWITTER_ACCESS_TOKEN_KEY,
            settings.TOKEN_TWITTER_ACCESS_TOKEN_SECRET
    )

    return t_api

def twitter_update(db_table, user_id, twitter_user_id):

    # getting last recorded tweet
    result = db_table.find({"type": "twitter", "user_id": user_id, "social_user_id": twitter_user_id,}).sort("time", -1).limit(1)

    since_id = 1

    if result.count() > 0:
        since_id = result.next()["post"]["id_str"]



    t_params = {"user_id": twitter_user_id, "trim_user": "true", "count": 200, "since_id": since_id}

    print("core/twitter: statuses/user_timeline - ", t_params)
    t_response = getTwitterAPI().request('statuses/user_timeline', t_params)


    processed_posts = 0

    for item in t_response:

        if "media" in item['entities']:
            for media in item['entities']['media']:
                media["local_url"] = cache_file(media['media_url'])

        created_at = int(time.mktime(time.strptime(str(item['created_at']), "%a %b %d %H:%M:%S +0000 %Y")))

        # not optimized 200 reqs to db. but need for unexpected script termination
        db_table.insert({"type":"twitter", "user_id": user_id, "social_user_id": twitter_user_id, "time": created_at, "post": item})

        processed_posts += 1

    return processed_posts
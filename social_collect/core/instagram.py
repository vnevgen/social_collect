__author__ = 'vitaly'

from django.conf import settings
from .api_wrap import api_wrapper

from ..filesystem import cache_file

def InstagramAPI(method, params={}):
    params['access_token'] = settings.TOKEN_INSTAGRAM
    params['v'] = '5.14'
    url = 'https://api.instagram.com/v1/%s' % method

    print("core/instagram: %s - %s" % (method, params))
    return api_wrapper(url, params)


def instagram_update(db_table, user_id, instagram_user_id):


    # getting last recorded instagram post
    result = db_table.find({"type": "instagram", "user_id": user_id, "social_user_id": instagram_user_id}).sort("time", -1).limit(1)

    min_id = "%s_%s" % (1, instagram_user_id)

    if result.count() > 0:
        min_id = result.next()["post"]["id"]

        post_id = int(min_id.split("_")[0]) + 1
        min_id = "%s_%s" % (post_id, instagram_user_id)

    i_response = InstagramAPI("users/%s/media/recent" % instagram_user_id, {"count": 33, "min_id": min_id})

    processed_posts = 0

    for item in i_response['data']:


        sr = item['images']['standard_resolution']
        sr['local_url'] = cache_file(sr['url'])

        created_time = int(item['created_time'])

        # not optimized 33 reqs to db. but need for unexpected script termination
        db_table.insert({"type":"instagram", "user_id": user_id, "social_user_id": instagram_user_id, "time": created_time, "post": item})

        processed_posts += 1

    return processed_posts
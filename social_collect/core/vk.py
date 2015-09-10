__author__ = 'vitaly'

from django.conf import settings
from .api_wrap import api_wrapper

from ..filesystem import cache_file

def VKAPI(method, params={}):
    params['access_token'] = settings.TOKEN_VK
    params['v'] = '5.37'
    url = 'https://api.vk.com/method/%s' % method

    print("core/vk: %s - %s" % (method, params))
    return api_wrapper(url, params)['response']


def vk_update(db_table, user_id, vk_user_id):



    # getting last recorded instagram post
    result = db_table.find({"type": "vk", "user_id": user_id, "social_user_id": vk_user_id,}).sort("time", -1).limit(1)

    # need to optimize this block to make 1 req (not 2)

    last_db_post = 0
    last_post_id = 0

    if result.count() > 0:
        last_db_post = int(result.next()["post"]["id"])

        v_response = VKAPI("wall.get", {"count": 2, "offset": 0, "owner_id": vk_user_id, "filter": "owner"})

        items = v_response['items']

        # if we have posts
        if len(items) > 0:

            # determine last post id in VK
            last_post_id = int(items[0]['id'])

            # if last post is pinned
            if items[0].get('is_pinned', False):

                # check have more than one post (except pinned)
                if len(items) > 1:

                    # if second post have greater ID set it as last_post_id
                    if int(items[1]['id']) > last_post_id:
                        last_post_id = int(items[1]['id'])


            # check if have new posts
            if last_post_id <= last_db_post:
                # no new posts added
                return 0

        else:
            # no posts at all
            return 0

    print("last post id", last_post_id)

    # here starting parsing posts

    v_response = VKAPI("wall.get", {"count": 100, "offset": 0, "owner_id": vk_user_id, "filter": "owner"})

    processed_posts = 0


    for item in v_response['items']:

        is_pinned = item.get('is_pinned', False)

        # end loop when got old posts (except pinned)
        if item['id'] <= last_db_post and not is_pinned:
            break

        if item['id'] <= last_db_post and is_pinned:
            continue


        def process_attachments(attachments):
            for attachment in attachments:

                at_type = attachment.get('type')

                if at_type == "photo":

                    max_size = 0

                    for at_prop in attachment['photo']:
                        if "photo" in at_prop:

                            curr = int(at_prop.split("photo_")[1])

                            if curr > max_size:
                                max_size = curr


                    prop = "photo_%s" % max_size

                    attachment['photo']['local_url'] = cache_file(attachment['photo'][prop])

                elif at_type == "audio":

                    # TODO: unknown url type: ''

                    attachment["audio"]["local_url"] = cache_file(attachment["audio"]["url"])

                elif at_type == "link":
                    # TODO: add link parse
                    pass



        if item.get('attachments', False):
            process_attachments(item['attachments'])

        if item.get('copy_history', False):

            for repost in item['copy_history']:

                if repost.get('attachments', False):
                    process_attachments(repost['attachments'])





        date = int(item['date'])

        # not optimized 33 reqs to db. but need for unexpected script termination
        db_table.insert({"type":"vk", "user_id": user_id, "time": date, "social_user_id": vk_user_id, "post": item})

        processed_posts += 1





    return processed_posts
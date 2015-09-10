__author__ = 'vitaly'

from django.conf import settings
from .models import Person

from urllib.parse import urlsplit

from .filesystem import cache_file

def update():
    db_table = settings.MONGO_DB[settings.MONGO_TABLE_NAME]

    processed_posts = 0

    for person in Person.objects.all():
    # for person in Person.objects.all()[:1]:

        user_id = person.pk

        for account in person.accounts.all():

            account_social_id = account.social_id

            if account.type == "twitter":

                from .core.twitter import twitter_update
                processed_posts += twitter_update(db_table, user_id, account_social_id)

                pass

            elif account.type == "instagram":

                from .core.instagram import instagram_update
                processed_posts += instagram_update(db_table, user_id, account_social_id)

                pass

            elif account.type == "vk":

                from .core.vk import vk_update
                processed_posts += vk_update(db_table, user_id, account_social_id)

                pass

    return processed_posts


def remove_user_posts(type, user_id, social_user_id):

    db_table = settings.MONGO_DB[settings.MONGO_TABLE_NAME]

    result = db_table.remove({"type": type, "user_id": user_id, "social_user_id": social_user_id})

    # FIXME: but files are not deleted

    if not result.get('ok', False):
        return False

    return True



def fetch_link(link):

    domain = "{0.netloc}".format(urlsplit(link))
    query = "{0.path}".format(urlsplit(link))[1:].split('/')[0]

    try:

        if domain == "twitter.com":

            from .core.twitter import getTwitterAPI

            data = getTwitterAPI().request('users/show', {"screen_name": query, "include_entities": False}).json()

            if data.get('errors', False):
                return None

            image_url = data.get('profile_image_url').replace('_normal', '_bigger')

            account = {
                "type": "twitter",
                "screen_name": data.get('screen_name'),
                "social_id": data.get('id_str'),
                "name": data.get('name'),
                "image": cache_file(image_url)
            }

            return account


        elif domain == "vk.com":

            from .core.vk import VKAPI
            data = VKAPI("users.get", {"user_ids": query, "fields": "photo_50,photo_100,domain"})

            user = None

            for item in data:
                if item.get('domain') == query:
                    user = item
                    break

            if not user:
                return None

            image_url = user.get("photo_100", user.get("photo_50"))

            account = {
                "type": "vk",
                "screen_name": user['domain'],
                "social_id": user['id'],
                "name": "%s %s" % (user['first_name'], user['last_name']),
                "image": cache_file(image_url)
            }

            return account


        elif domain == "instagram.com":

            from .core.instagram import InstagramAPI
            data = InstagramAPI("users/search", {"q": query}).get('data')

            user = None

            for item in data:
                if item.get('username') == query:
                    user = item
                    break

            if not user:
                return None

            account = {
                "type": "instagram",
                "screen_name": user['username'],
                "social_id": user['id'],
                "name": user['full_name'],
                "image": cache_file(user['profile_picture'])
            }

            return account

        else:
            return None

    except:
        return None
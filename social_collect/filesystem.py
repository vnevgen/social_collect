__author__ = 'vitaly'

from django.conf import settings

import urllib.request
import gridfs


from urllib.parse import urlsplit



def cache_file(file_url):

    import os
    import time

    db = settings.MONGO_DB
    fs = gridfs.GridFS(db)

    write_url = "{0.netloc}/{0.path}".format(urlsplit(file_url))

    import hashlib
    m = hashlib.md5()
    m.update(write_url.encode('utf-8'))
    hash = m.hexdigest()


    if fs.exists(hash=hash):
        # already cached
        return hash


    print("cache_file: caching %s..." % file_url[:80])
    try:
        response = urllib.request.urlopen(file_url)
        data = response.read()

        content_type=response.info().get_content_type()

        with fs.new_file(hash=hash, content_type=content_type) as fp:
           fp.write(data)
    except:
        hash = ""

    return hash

def get_file(hash):

    db = settings.MONGO_DB
    fs = gridfs.GridFS(db)

    if not fs.exists(hash=hash):
        return False

    return fs.get_last_version(hash=hash)
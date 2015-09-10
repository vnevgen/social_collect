__author__ = 'vitaly'

from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError
import json
import time


def api_wrapper(url, params):

    params_compiled = urlencode(params)

    url = '%s?%s' % (url, params_compiled)

    req = Request(url)

    try:
        response = urlopen(req)
        body = response.read().decode(response.headers.get_content_charset())
        return json.loads(body)

    except HTTPError as e:
        print('Error code: ', e.code)
        exit()
    except URLError as e:
        print('Reason: ', e.reason)
        exit()
    except:
        print('something wrong happened')
        exit()
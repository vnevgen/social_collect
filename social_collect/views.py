__author__ = 'vitaly'

from django.http.response import HttpResponse, HttpResponseNotFound




from django.conf import settings

from .models import Person, PersonAccount

from .filesystem import cache_file, get_file


def test(request):


    db = settings.MONGO_DB


    from .core.instagram import InstagramAPI

    print(InstagramAPI("users/search", {"q": "Vitaly Nevgen"}))


    response = "not caching| okok"


    return HttpResponse(response, content_type="text/plain")

from django.shortcuts import render


def resolve_user(username_or_id):

    if username_or_id.isdigit():
        try:
            person = Person.objects.get(pk=username_or_id)
        except Person.DoesNotExist:
            return None
    else:
        # FIXME: here got a future problem of equal screen_names in different social networks
        accounts = PersonAccount.objects.filter(screen_name=username_or_id)

        if accounts.count() > 0:
            person = accounts[0].person
        else:
            return None

    return person


def feed(request, username_or_id):

    person = resolve_user(username_or_id)

    if not person:
        return HttpResponseNotFound("The requested user can't be found<br/><a href=\"/\">Return to index</a>")

    accounts = person.accounts.all()

    accounts_data = {}

    for account in accounts:
        accounts_data[account.type] = account

    # TODO: optimize list generator below

    db_table = settings.MONGO_DB[settings.MONGO_TABLE_NAME]
    db_query = {"type": {"$in": [account.type for account in accounts]}, "user_id": person.pk}


    feed_data = db_table.find(db_query).sort("time", -1).limit(50)

    template_vars = {
        "name": person.name,
        "feed_data": feed_data,
        "accounts": accounts_data,
        "accounts_arr": accounts,
        "user_id": person.pk
    }

    return render(request, "feed/feed.html", template_vars)

def person_list(request):

    persons = Person.objects.all()

    return render(request, "person/list.html", {"persons": persons})

def person_add(request):
    return render(request, "person/add.html", {})

def person_edit(request, username_or_id):

    person = resolve_user(username_or_id)

    if not person:
        HttpResponseNotFound("The requested user can't be found")


    accounts = person.accounts.all()

    return render(request, "person/edit.html", {"person": person})



def update(request):

    import json

    from .core_functions import update

    processed_posts = update()

    return HttpResponse(json.dumps({"processed_posts": processed_posts}))



def serve(request, filename):

    from urllib.parse import urlencode

    # dirty hack

    compiled_params = urlencode(request.GET)

    if compiled_params:
        filename = "%s?%s" % (filename, compiled_params)


    fp = get_file(filename)

    if not fp:
        return HttpResponseNotFound("The requested file can\'t be found. Sorry about it :(<hr>self-static server v0.1")


    return HttpResponse(fp.read(), fp.content_type)

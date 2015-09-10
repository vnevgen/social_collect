from django.conf.urls import include, url
from django.contrib import admin

from .views import test, serve, update, feed
from .views import person_edit, person_list, person_add

from django.views.generic.base import RedirectView
from django.views.generic import TemplateView

from .api import PersonView, PersonDetailView, set_image, AccountListView, AccountDetailView


username_or_id = r'(?P<username_or_id>[^/]{1,128})'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test$', test),



    url(r'^$', person_list),
    url(r'^person/add$', person_add),
    url(r'^person/' + username_or_id + r'$', feed),
    url(r'^person/' + username_or_id + r'/edit$', person_edit),

    url(r'^getfile/(?P<filename>[^/]{1,128})$', serve),

    url(r'^api/v1/update$', update),

    url(r'^api/v1/person$', PersonView.as_view()),
    url(r'^api/v1/person/(?P<pk>\d+)$', PersonDetailView.as_view()),


    url(r'^api/v1/person/(?P<pk>\d+)/account$', AccountListView.as_view()),

    url(r'^api/v1/person/(?P<pk>\d+)/account/(?P<account_pk>\d+)$', AccountDetailView.as_view()),
    url(r'^api/v1/person/(?P<pk>\d+)/account/(?P<account_pk>\d+)/set-image$', set_image),

    url(r'^.*$', RedirectView.as_view(url='/', permanent=False), name='index')

]

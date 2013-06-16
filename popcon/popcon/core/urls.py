from django.conf.urls import patterns, include, url

from .views import Publish, AppInfo, AppsList, Ranking

urlpatterns = patterns('',
    url(r'publish/(?P<uuid>[0-9a-f]{32})/$', Publish.as_view(), name='publish'),
    url(r'info/(?P<name>[A-Za-z0-9_-]+)/$', AppInfo.as_view(), name='info'),
    url(r'list/$', AppsList.as_view(), name='list'),
    url(r'ranking/$', Ranking.as_view(), name='ranking'),
)

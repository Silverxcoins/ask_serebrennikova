from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from ask import views



urlpatterns = [ 
    url(r'^signup/?', views.signup, name='signup'),
    url(r'^login/?', views.login, name='login'),
    url(r'^logout/?', views.logout, name='logout'),
    url(r'^ask/?', views.ask, name='ask'),
    url(r'^profile/edit?', views.settings, name='settings'),
    url(r'^hot/(?P<page>\d+)?/?', views.hot, name = 'hot'),
    url(r'^tag/(?P<tag_name>[^/]+)?/?(?P<page>\d+)?/?', views.tag, name = 'tag'),
    url(r'^question/(?P<question_id>\d+)?/?(?P<page>\d+)?/?', views.question, name='question'),
    url(r'^like/?', views.like, name='like'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<page>\d+)?/?', views.index, name='index'),
]

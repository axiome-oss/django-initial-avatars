from django.conf.urls import  include, url

urlpatterns = [ 
	url(r'^(?P<id>[0-9]+)/$', 'initial_avatars.views.avatar', name='avatar'),
	url(r'^(?P<id>[0-9]+)/(?P<size>[0-9]{2,3})/$', 'initial_avatars.views.avatar', name='avatar'),
]
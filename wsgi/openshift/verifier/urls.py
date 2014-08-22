from django.conf.urls import patterns, url
from verifier.views import UserView

urlpatterns = patterns('',
    url(r'^/user/(?P<username>\w+)/', UserView.as_view(), name='single_user_view'),

    )
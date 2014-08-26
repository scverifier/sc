from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from verifier.models import UserType, Subreddit, RedditCredentials
from verifier.views import UserTypeEditView, UserTypeListView, SubredditEditView, CredentialsView, CredentialsListView, \
    UserTypeSubredditsView

urlpatterns = patterns('',
    # Examples:
    url(r'^/usertypes/new$', UserTypeEditView.as_view(), name='usertype_create'),
    url(r'^/usertypes/(?P<pk>\d+)/subreddits', UserTypeSubredditsView.as_view(), name='usertype_subreddits'),
    url(r'^/usertypes/(?P<pk>\d+)', UserTypeEditView.as_view(), name='usertype_edit'),
    url(r'^/usertypes', login_required(ListView.as_view(
        model=UserType, template_name='verifier/usertypes.html')), name='usertype_list'),

    url(r'^/subreddits/new$', SubredditEditView.as_view(), name='subreddit_create'),
    url(r'^/subreddits/(?P<pk>\d+)', SubredditEditView.as_view(), name='subreddit_edit'),
    url(r'^/subreddits', login_required(ListView.as_view(
        model=Subreddit, template_name='verifier/subreddits.html')), name='subreddit_list'),

    url(r'^/credentials/new$', CredentialsView.as_view(), name='credentials_create'),
    url(r'^/credentials/(?P<pk>\d+)', CredentialsView.as_view(), name='credentials_edit'),
    url(r'^/credentials', CredentialsListView.as_view(), name='credentials_list'),
)

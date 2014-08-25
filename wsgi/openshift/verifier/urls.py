from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from verifier.models import Gender, Subreddit, RedditCredentials
from verifier.views import GenderEditView, GenderListView, SubredditEditView, CredentialsView, CredentialsListView, \
    GenderSubredditsView

urlpatterns = patterns('',
    # Examples:
    url(r'^/genders/new$', GenderEditView.as_view(), name='gender_create'),
    url(r'^/genders/(?P<pk>\d+)/subreddits', GenderSubredditsView.as_view(), name='gender_subreddits'),
    url(r'^/genders/(?P<pk>\d+)', GenderEditView.as_view(), name='gender_edit'),
    url(r'^/genders', login_required(ListView.as_view(
        model=Gender, template_name='verifier/genders.html')), name='gender_list'),

    url(r'^/subreddits/new$', SubredditEditView.as_view(), name='subreddit_create'),
    url(r'^/subreddits/(?P<pk>\d+)', SubredditEditView.as_view(), name='subreddit_edit'),
    url(r'^/subreddits', login_required(ListView.as_view(
        model=Subreddit, template_name='verifier/subreddits.html')), name='subreddit_list'),

    url(r'^/credentials/new$', CredentialsView.as_view(), name='credentials_create'),
    url(r'^/credentials/(?P<pk>\d+)', CredentialsView.as_view(), name='credentials_edit'),
    url(r'^/credentials', CredentialsListView.as_view(), name='credentials_list'),
)

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from verifier.models import Gender, Subreddit
from verifier.views import GenderCreateView, GenderListView

urlpatterns = patterns('',
    # Examples:
    url(r'^/genders/new$', GenderCreateView.as_view(), name='gender_create'),
    url(r'^/genders/(?P<pk>\d+)', GenderCreateView.as_view(), name='gender_edit'),
    url(r'^/genders', login_required(ListView.as_view(
        model=Gender, template_name='verifier/genders.html')), name='gender_list'),
    url(r'^/subreddits', login_required(ListView.as_view(
        model=Subreddit, template_name='verifier/subreddits.html')), name='subreddit_list'),
)

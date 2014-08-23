from django.conf.urls import patterns, url
from verifier.views import GenderCreateView, GenderListView

urlpatterns = patterns('',
    # Examples:
    url(r'^/genders/new$', GenderCreateView.as_view(), name='gender_create'),
    url(r'^/genders/(?P<pk>\d+)', GenderCreateView.as_view(), name='gender_edit'),
    url(r'^/genders', GenderListView.as_view(), name='gender_edit'),
)

from django.conf.urls import patterns, url
from verifier.views import GenderCreateView

urlpatterns = patterns('',
    # Examples:
    url(r'^/gender$', GenderCreateView.as_view(), name='gender_create'),
    url(r'^/gender/(?P<pk>\d+)', GenderCreateView.as_view(), name='gender_edit'),
    url(r'^/gender/', GenderCreateView.as_view(), name='gender_edit'),
)

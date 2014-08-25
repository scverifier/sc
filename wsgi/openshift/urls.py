from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from verifier.views import VerificationView, LoginView, CredentialsView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', VerificationView.as_view(), name='home'),
    # url(r'^verify$', login_required(VerificationView.as_view()), name='verify'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout',
        dict(template_name='verifier/logged_out.html', next_page='/')),
    url(r'^api', include('api.urls')),
    url(r'^data', include('verifier.urls')),
    # url(r'^$', 'openshift.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
)

from django.conf import settings

# Create your views here.
from django.http.response import HttpResponseRedirect
from django.views.generic import FormView, CreateView
from django.views.generic.base import RedirectView
from praw import Reddit
from requests import HTTPError
from rest_framework.views import APIView
from rest_framework.response import Response
from verifier.forms import VerificationForm, GenderForm
from verifier.models import Gender


class VerificationView(FormView):
    form_class = VerificationForm
    template_name = "verifier/verify.html"
    success_url = '/'

    def form_valid(self, form):
        form.verify()
        return super(VerificationView, self).form_valid(form)


class UserView(APIView):

    def get(self, *args, **kwargs):
        username = self.kwargs['username']
        api = Reddit(user_agent=settings.USER_AGENT)
        exists = False
        redditor = None
        try:
            redditor = api.get_redditor(username)
            exists = True
        except HTTPError:
            exists = False
        data = {'exists': exists}
        if redditor:
            data['redditor'] = redditor.fullname
        return Response(data)


class GenderCreateView(FormView):
    form_class = GenderForm
    template_name = 'verifier/gender.html'
    success_url = '/'
    gender = None

    def get_initial(self):
        initial = super(GenderCreateView, self).get_initial()

        if self.gender:
            initial['name'] = self.gender.name
            initial['css_class'] = self.gender.css_class
            initial['subreddits'] = '\r\n'.join((s.name for s in self.gender.subreddits.all()))
        return initial

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        if pk:
            try:
                self.gender = Gender.objects.get(pk=pk)
            except:
                return HttpResponseRedirect('/')
        return super(GenderCreateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        pk = self.kwargs.get('pk', None)

        form.save(pk)

        return super(GenderCreateView, self).form_valid(form)
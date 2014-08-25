import django
from django.conf import settings

# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden, Http404
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from praw import Reddit
from requests import HTTPError
from rest_framework.views import APIView
from rest_framework.response import Response
import verifier.forms as verifier_forms
import verifier.models as models


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class LoginView(FormView):
    form_class = verifier_forms.LoginForm
    template_name = 'verifier/login.html'
    success_url = '/'

    def form_valid(self, form):
        username, password = form.cleaned_data['username'], form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        if 'next' in self.request.GET:
            return HttpResponseRedirect(self.request.GET['next'])
        return super(LoginView, self).form_valid(form)


class VerificationView(LoginRequiredMixin, FormView):
    form_class = verifier_forms.VerificationForm
    template_name = "verifier/verify.html"
    success_url = '/'

    def form_valid(self, form):
        #TODO: implement verification
        # form.verify()
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


class GenderEditView(LoginRequiredMixin, UpdateView):
    form_class = verifier_forms.GenderForm
    model = models.Gender
    template_name = 'verifier/gender.html'
    success_url = '/data/genders'
    gender = None

    def get_object(self, queryset=None):
        if not 'pk' in self.kwargs:
            return None
        try:
            return models.Gender.objects.get(pk=self.kwargs['pk'])
        except models.Gender.DoesNotExist:
            raise Http404


class GenderListView(LoginRequiredMixin, ListView):
    model = models.Gender
    template_name = 'verifier/genders.html'


class SubredditEditView(LoginRequiredMixin, UpdateView):
    model = models.Subreddit
    template_name = 'verifier/subreddit.html'
    success_url = '/data/subreddits'
    form_class = verifier_forms.SubredditForm

    def get_object(self, queryset=None):
        if not 'pk' in self.kwargs:
            return None
        try:
            return models.Subreddit.objects.get(pk=self.kwargs['pk'])
        except models.Subreddit.DoesNotExist:
            raise Http404


class CredentialsView(LoginRequiredMixin, UpdateView):
    model = models.RedditCredentials
    template_name = 'verifier/credentials.html'
    success_url = '/'
    form_class = verifier_forms.CredentialsForm

    def get_object(self, queryset=None):
        user = self.request.user
        credentials, created = models.RedditCredentials.\
            objects.get_or_create(user=user)
        return credentials
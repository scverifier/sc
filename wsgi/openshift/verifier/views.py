from django.conf import settings

# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.generic import FormView
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


class GenderEditView(LoginRequiredMixin, FormView):
    form_class = verifier_forms.GenderForm
    template_name = 'verifier/gender.html'
    success_url = '/data/genders'
    gender = None

    def get_form_kwargs(self):
        kwargs = super(GenderEditView, self).get_form_kwargs()
        if self.gender:
            kwargs['instance'] = self.gender
        return kwargs

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        if pk:
            try:
                self.gender = models.Gender.objects.get(pk=pk)
            except:
                return HttpResponseNotFound()
        return super(GenderEditView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        pk = self.kwargs.get('pk', None)

        form.save(pk)

        return super(GenderEditView, self).form_valid(form)


class GenderListView(LoginRequiredMixin, ListView):
    model = models.Gender
    template_name = 'verifier/genders.html'


class SubredditEditView(LoginRequiredMixin, FormView):
    model = models.Subreddit
    template_name = 'verifier/subreddit.html'
    success_url = '/data/subreddits'
    form_class = verifier_forms.SubredditForm

    def get_form_kwargs(self):
        kwargs = super(SubredditEditView, self).get_form_kwargs()
        if 'pk' in self.kwargs:
            subreddit = models.Subreddit.objects.get(id=self.kwargs['pk'])
            kwargs['instance'] = subreddit
        return kwargs

    def get(self, request, *args, **kwargs):
        try:
            return super(SubredditEditView, self).get(request, *args, **kwargs)
        except models.models.exceptions.ObjectDoesNotExist:
            return HttpResponseNotFound()

    def form_valid(self, form):
        form.save()
        return super(SubredditEditView, self).form_valid(form)
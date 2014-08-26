import django
from django.conf import settings

# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden, Http404
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.views.generic.base import View
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


class StaffRequiredMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)


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

    def get_form(self, form_class):
        form = super(VerificationView, self).get_form(form_class)
        form.current_user = self.request.user
        return form

    def form_valid(self, form):
        context = self.get_context_data(form=verifier_forms.VerificationForm())
        print(context['form'])
        context['verification_success'] = True
        context['verified_user'] = form.cleaned_data['username']
        return self.render_to_response(context)



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


class UserTypeEditView(LoginRequiredMixin, UpdateView):
    form_class = verifier_forms.UserTypeForm
    model = models.UserType
    template_name = 'verifier/usertype.html'
    success_url = '/data/usertypes'
    usertype = None

    def get_object(self, queryset=None):
        if not 'pk' in self.kwargs:
            return None
        try:
            return models.UserType.objects.get(pk=self.kwargs['pk'])
        except models.UserType.DoesNotExist:
            raise Http404


class UserTypeListView(LoginRequiredMixin, ListView):
    model = models.UserType
    template_name = 'verifier/usertypes.html'


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


class CredentialsView(StaffRequiredMixin, UpdateView):
    model = models.RedditCredentials
    template_name = 'verifier/credentials.html'
    success_url = '/data/credentials'
    form_class = verifier_forms.CredentialsForm

    def get_object(self, queryset=None):
        if not 'pk' in self.kwargs:
            return None
        try:
            return models.RedditCredentials.objects.get(pk=self.kwargs['pk'])
        except models.RedditCredentials.DoesNotExist:
            raise Http404


class UserTypeSubredditsView(LoginRequiredMixin, FormView):
    form_class = verifier_forms.UserTypeSubredditsForm
    template_name = 'verifier/usertype_subreddits.html'
    success_url = '/data/usertypes'
    _subreddits = None
    _usertype = None

    @property
    def usertype(self):
        if self._usertype:
            return self._usertype
        pk = self.kwargs['pk']
        try:
            self._usertype = models.UserType.objects.get(pk=pk)
        except models.UserType.DoesNotExist:
            raise Http404
        return self._usertype

    @property
    def subreddits(self):
        self._subreddits = self.usertype.subreddits.all()
        return self._subreddits
    
    def get_form(self, form_class):
        form = super(UserTypeSubredditsView, self).get_form(form_class)
        subreddits = self.subreddits
        form.init_subreddits_list(subreddits)
        return form

    def get_initial(self):
        initial = super(UserTypeSubredditsView, self).get_initial()
        for usertype_subreddit in self.usertype.usertypesubreddit_set.all():
            text_field_name = verifier_forms.\
                UserTypeSubredditsForm.\
                get_text_field_name(usertype_subreddit.subreddit.id)
            css_field_name = verifier_forms.\
                UserTypeSubredditsForm.\
                get_css_field_name(usertype_subreddit.subreddit.id)

            initial[text_field_name] = usertype_subreddit.flair_text
            initial[css_field_name] = usertype_subreddit.flair_css
        return initial

    def form_valid(self, form):
        form.save(self.usertype.usertypesubreddit_set.all())
        return super(UserTypeSubredditsView, self).form_valid(form)


class CredentialsListView(StaffRequiredMixin, ListView):
    model = models.RedditCredentials
    template_name = 'verifier/credentials_list.html'

    def get_queryset(self):
        return models.RedditCredentials.objects.all()
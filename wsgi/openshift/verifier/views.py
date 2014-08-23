from django.conf import settings

# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views.generic import FormView, CreateView
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from praw import Reddit
from requests import HTTPError
from rest_framework.views import APIView
from rest_framework.response import Response
from verifier.forms import VerificationForm, GenderForm, LoginForm
from verifier.models import Gender, Subreddit

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class VerificationView(LoginRequiredMixin, FormView):
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


class GenderCreateView(LoginRequiredMixin, FormView):
    form_class = GenderForm
    template_name = 'verifier/gender.html'
    success_url = '/data/genders'
    gender = None

    def get_initial(self):
        initial = super(GenderCreateView, self).get_initial()

        if self.gender:
            initial['name'] = self.gender.name
        return initial

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        if pk:
            try:
                self.gender = Gender.objects.get(pk=pk)
            except:
                return HttpResponseNotFound()
        return super(GenderCreateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        pk = self.kwargs.get('pk', None)

        form.save(pk)

        return super(GenderCreateView, self).form_valid(form)


class GenderListView(ListView):
    model = Gender
    template_name = 'verifier/genders.html'


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'verifier/login.html'
    # success_url = '/'

    def form_valid(self, form):
        username, password = form.cleaned_data['username'], form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        if 'next' in self.request.GET:
            return HttpResponseRedirect(self.request.GET['next'])
        return super(LoginView, self).form_valid(form)
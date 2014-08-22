from django.conf import settings

# Create your views here.
from django.views.generic import FormView
from praw import Reddit
from requests import HTTPError
from rest_framework.views import APIView
from rest_framework.response import Response
from verifier.forms import VerificationForm


class VerificationView(FormView):
    form_class = VerificationForm
    template_name = "verify.html"
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

from django.shortcuts import render

# Create your views here.
from praw import Reddit
from requests import HTTPError
from rest_framework.response import Response
from rest_framework.views import APIView
import settings


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
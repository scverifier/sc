from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.base import Model
import django.db.models as models


class Subreddit(Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Gender(Model):
    name = models.CharField(max_length=64)
    subreddits = models.ManyToManyField(Subreddit, through='GenderSubreddit')

    def __str__(self):
        return self.name


class GenderSubreddit(Model):
    gender = models.ForeignKey(Gender)
    subreddit = models.ForeignKey(Subreddit)
    flair_css = models.CharField(max_length=128, null=True)
    flair_text = models.CharField(max_length=128, null=True)

    def __str__(self):
        return '{0} - {1}'.format(self.gender, self.subreddit)


class Verification(Model):
    username = models.CharField(max_length=128)
    gender = models.ForeignKey(Gender)
    verified_by = models.ForeignKey(User)
    verified_on = models.DateTimeField(auto_now=True)
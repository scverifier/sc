from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.base import Model
import django.db.models as models


class RedditCredentials(Model):
    reddit_username = models.CharField(max_length=256, blank=True)
    reddit_password = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.reddit_username


class Subreddit(Model):
    name = models.CharField(max_length=128)
    credentials = models.ForeignKey(RedditCredentials)

    def __str__(self):
        return self.name


class UserType(Model):
    name = models.CharField(max_length=64)
    subreddits = models.ManyToManyField(Subreddit, through='UserTypeSubreddit')

    def __str__(self):
        return self.name


class UserTypeSubreddit(Model):
    usertype = models.ForeignKey(UserType)
    subreddit = models.ForeignKey(Subreddit)
    flair_css = models.CharField(max_length=128, null=True, blank=True)
    flair_text = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        unique_together = ('usertype', 'subreddit')

    def __str__(self):
        return '{0} - {1}'.format(self.usertype, self.subreddit)


class Verification(Model):
    username = models.CharField(max_length=128)
    usertype = models.ForeignKey(UserType)
    verified_by = models.ForeignKey(User)
    verified_on = models.DateTimeField(auto_now=True)
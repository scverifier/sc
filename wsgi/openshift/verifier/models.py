from django.db import models

# Create your models here.
from django.db.models.base import Model
from django.db.models.fields.related import ManyToManyField
import django.db.models as models


class Subreddit(Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Gender(Model):
    name = models.CharField(max_length=64)
    css_class = models.CharField(max_length=64)
    subreddits = models.ManyToManyField(Subreddit)

    def __str__(self):
        return self.name
from django.db import models

# Create your models here.
from django.db.models.base import Model
from django.db.models.fields.related import ManyToManyField
from django.forms.fields import CharField


class Gender(Model):
    name = CharField(max_length=64)
    css_class = CharField(max_length=64)


class Subreddit(Model):
    name = CharField(max_length=128)
    gender = ManyToManyField(Gender)
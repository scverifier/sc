from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms as forms
from django.contrib.auth import authenticate
from django.db import transaction
from django.forms.fields import CharField, ChoiceField
from django.forms.forms import Form
import django.forms.models as django_models
import django.forms.widgets as widgets
from praw import Reddit

import verifier.models as models


class DefaultFormHelper(FormHelper):
    def __init__(self, submit_text, *args, **kwargs):
        super(DefaultFormHelper, self).__init__(*args, **kwargs)
        self.form_class = 'form-standard'
        self.error_text_inline = False
        self.add_input(Submit('submit', submit_text, css_class='btn btn-lg btn-primary btn-block'))


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=widgets.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = DefaultFormHelper('Log in')

    def is_valid(self):
        result = super(LoginForm, self).is_valid()
        if result:
            username, password = (self.cleaned_data[x] for x in ('username', 'password'))
            user = authenticate(username=username, password=password)
            if not user:
                self.errors['password'] = ['Invalid username or password.']
                result = False
        return result


class VerificationForm(Form):
    username = CharField()
    # gender = ChoiceField(widget=RadioSelect)

    def __init__(self, *args, **kwargs):
        super(VerificationForm, self).__init__(*args, **kwargs)
        choices = [(g.id, g) for g in models.Gender.objects.all()]
        self.fields['gender'] = ChoiceField(widget=widgets.RadioSelect, choices=choices)

    def verify(self):
        username = self.cleaned_data['username']
        gender = self.cleaned_data['gender']
        print(username, gender)
        api = Reddit(user_agent='ssutekh/verifier_0.1a')
        api.login('ssutekh', 'mastercard1')
        print('Logged in')
        subreddit = api.get_subreddit('ssutekh_test')
        print('Fetched subreddit')
        subreddit.remove_contributor(username)
        print('Contributor added')
        api.set_flair(subreddit, username, gender)
        print('Flair set')


class GenderForm(django_models.ModelForm):
    class Meta:
        model = models.Gender

    name = CharField()
    subreddits = django_models.ModelMultipleChoiceField(queryset=models.Subreddit.objects.all(),
                                          widget=widgets.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance', None):
            instance = kwargs['instance']
            initial = kwargs.setdefault('initial', {})
            initial['name'] = instance.name
            initial['subreddits'] = instance.subreddits.all()
        super(GenderForm, self).__init__(*args, **kwargs)

        self.helper = DefaultFormHelper('Save')

    @transaction.atomic
    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        instance.save()
        instance.name = self.cleaned_data['name']
        subreddits = self.cleaned_data['subreddits']

        self.save_subreddits(instance, subreddits)

        return instance

    def save_subreddits(self, gender, subreddits):
        models.GenderSubreddit.objects \
            .filter(gender=gender) \
            .exclude(subreddit__in=subreddits) \
            .delete()
        new_subreddits = filter(lambda s: s not in gender.subreddits.all(), subreddits)
        for subreddit in new_subreddits:
            gs = models.GenderSubreddit()
            gs.gender = gender
            gs.subreddit = subreddit
            gs.save()
        gender.save()


class SubredditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        self.helper = DefaultFormHelper('Save')
        super(SubredditForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Subreddit
        fields = [
            'name',
            ]
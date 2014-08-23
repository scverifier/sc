from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms as forms
from django.contrib.auth import authenticate, login
from django.forms import widgets as widgets, ModelChoiceField
from django.forms.fields import CharField, ChoiceField
from django.forms.forms import Form
from django.forms.models import ModelMultipleChoiceField
from django.forms.widgets import RadioSelect, Textarea, CheckboxSelectMultiple, CheckboxChoiceInput, CheckboxInput
from praw import Reddit
from verifier.models import Gender, Subreddit, GenderSubreddit


class VerificationForm(Form):
    username = CharField()
    # gender = ChoiceField(widget=RadioSelect)
    
    def __init__(self, *args, **kwargs):
        super(VerificationForm, self).__init__(*args, **kwargs)
        choices = [(g.id, g) for g in Gender.objects.all()]
        self.fields['gender'] = ChoiceField(widget=RadioSelect, choices=choices)

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


class GenderForm(Form):
    name = CharField()
    subreddits = ModelMultipleChoiceField(queryset=Subreddit.objects.all(),
                                          widget=CheckboxSelectMultiple)
    
    def __init__(self, *args, **kwargs):
        super(GenderForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-standard'
        self.helper.error_text_inline = False
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-lg btn-primary btn-block'))

    def save(self, pk=None):
        print(pk)
        name = self.cleaned_data['name']
        subreddits = self.cleaned_data['subreddits']

        #TODO: implement subreddit saving logic

        gender.save()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=widgets.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-standard'
        self.helper.error_text_inline = False
        self.helper.add_input(Submit('submit', 'Log in', css_class='btn btn-lg btn-primary btn-block'))

    def is_valid(self):
        result = super(LoginForm, self).is_valid()
        if result:
            username, password = (self.cleaned_data[x] for x in ('username', 'password'))
            user = authenticate(username=username, password=password)
            if not user:
                self.errors['password'] = ['Invalid username or password.']
                result = False
        return result


from crispy_forms.bootstrap import FormActions, FieldWithButtons, StrictButton, Alert, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Button, Div, Column, HTML
from django import forms as forms
from django.contrib.auth import authenticate
from django.db import transaction
from django.forms.fields import CharField, ChoiceField
from django.forms.forms import Form
import django.forms.models as django_models
import django.forms.widgets as widgets
from praw import Reddit

import settings

import verifier.models as models


class DefaultFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(DefaultFormHelper, self).__init__(*args, **kwargs)
        self.form_class = 'form-standard'
        self.form_show_labels = False
        self.error_text_inline = False


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
    gender = ChoiceField(widget=widgets.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(VerificationForm, self).__init__(*args, **kwargs)

        self.helper = DefaultFormHelper()
        self.helper.form_id = 'verificationForm'
        self.helper.layout = Layout(
            Div(
                Div(
                    PrependedText(
                        'username',
                        '/u/',
                        placeholder='username',
                        css_class='input-lg',
                    ),
                    css_class='col-xs-4'
                ),
                Div(
                    StrictButton('Check',
                                 id='btnUsernameCheck',
                                 data_loading_text='Checking',
                                 css_class='btn-lg btn-info'),
                    css_class='col-xs-2',
                ),
                Div(
                    HTML('''<span id="spAlertUserExists" class="alert alert-success usercheck_alert">User exists</span>'''),
                    HTML('''<span id="spAlertUserNotExists" class="alert alert-danger usercheck_alert">User doesn't exist</span>'''),
                    css_class='col-l-4',
                    id='divAlertsContainer',
                ),

                css_class='row'
            ),
            'gender',
            Submit(
                'verify',
                'Verify',
                id='btnVerify',
                data_loading_text='Verifying',
                css_class='btn-lg btn-success',
                disabled='disabled',
            ),
        )
        choices = [(g.id, g) for g in models.Gender.objects.all()]
        self.fields['gender'].choices = choices


class GenderForm(django_models.ModelForm):
    class Meta:
        model = models.Gender
        fields = (
            'name',
            'subreddits',
        )

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

        self.helper = DefaultFormHelper()
        self.helper.layout = Layout(
            Field('name'),
            Field('subreddits', style='padding-left: 20px'),
            FormActions(
                Submit('save', 'Save', css_class='btn-primary'),
                Button('cancel', 'Cancel'),
            )
        )

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
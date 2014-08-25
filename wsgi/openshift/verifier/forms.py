from crispy_forms.bootstrap import FormActions, FieldWithButtons, StrictButton, Alert, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Button, Div, Column, HTML, Fieldset, Hidden
from django import forms as forms
from django.contrib.auth import authenticate
from django.db import transaction
from django.forms.fields import CharField, ChoiceField
from django.forms.forms import Form
import django.forms.models as django_models
import django.forms.widgets as widgets
from praw import Reddit

import settings
from verifier import verification

import verifier.models as models


class DefaultFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(DefaultFormHelper, self).__init__(*args, **kwargs)
        self.form_class = 'form-standard'
        self.error_text_inline = False


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=widgets.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = DefaultFormHelper()
        self.helper.add_input(Submit('login', 'Log in', css_class='btn btn-success btn-block'))

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
        self.helper.form_show_labels = False
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

    def verify(self, current_user):
        gender_id = self.cleaned_data['gender']

        gender = models.Gender.objects.get(pk=gender_id)
        username = self.cleaned_data['username']
        if not username in settings.TEST_USERNAMES:
            print('Non-test username %s, canceling verification.' % username)
            return

        #TODO: add verification failure, result logging and display
        for gs in gender.gendersubreddit_set.all():
            moderator_username = gs.subreddit.credentials.reddit_username
            moderator_password = gs.subreddit.credentials.reddit_password
            flair_text = gs.flair_text
            flair_css = gs.flair_css
            verification.verify(moderator_username,
                                moderator_password,
                                username,
                                gs.subreddit.name,
                                flair_text,
                                flair_css)
        v = models.Verification()
        v.username = username
        v.gender = gender
        v.verified_by = current_user
        v.save()



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
    class Meta:
        model = models.Subreddit
        fields = [
            'name',
            'credentials',
        ]

    def __init__(self, *args, **kwargs):
        super(SubredditForm, self).__init__(*args, **kwargs)
        self.helper = DefaultFormHelper()
        self.helper.add_input(Submit('save', 'Save', css_class='btn btn-success'))


class GenderSubredditsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(GenderSubredditsForm, self).__init__(*args, **kwargs)
        self.helper = DefaultFormHelper()
        self.helper.form_show_labels = False

    def init_subreddits_list(self, subreddits):
        layout = Layout()
        self.helper.layout = layout

        for subreddit in subreddits:
            flair_css_field_id = self.get_css_field_name(subreddit.id)
            flair_text_field_id = self.get_text_field_name(subreddit.id)
            self.fields[flair_css_field_id] = CharField(required=False)
            self.fields[flair_text_field_id] = CharField(required=False)
            fieldset = Fieldset(
                '/r/{0}:'.format(subreddit.name),
                Field(flair_css_field_id, placeholder='Flair CSS'),
                Field(flair_text_field_id, placeholder='Flair text'),
            )
            layout.append(fieldset)
        layout.append(
            FormActions(
                Submit('save', 'Save', css_class='btn-primary'),
                Button('cancel', 'Cancel'),
            )
        )

    @transaction.atomic
    def save(self, gender_subreddits):
        #TODO: verify that subreddit list hasn't changed between requests
        for gs in gender_subreddits:
            css_field_name = self.get_css_field_name(gs.subreddit.id)
            text_field_name = self.get_text_field_name(gs.subreddit.id)
            css = self.cleaned_data[css_field_name]
            text = self.cleaned_data[text_field_name]
            gs.flair_css = css
            gs.flair_text = text
            gs.save()

    def is_valid(self):
        return super(GenderSubredditsForm, self).is_valid()

    @staticmethod
    def get_text_field_name(subreddit_id):
        return 'subreddit_{0}.flair_text'.format(subreddit_id)

    @staticmethod
    def get_css_field_name(subreddit_id):
        return 'subreddit_{0}_flair_css'.format(subreddit_id)


class CredentialsForm(forms.ModelForm):
    reddit_username = CharField()
    reddit_password = CharField(widget=widgets.PasswordInput)

    class Meta:
        model = models.RedditCredentials
        fields = [
            'reddit_username',
            'reddit_password',
        ]

    def __init__(self, *args, **kwargs):
        super(CredentialsForm, self).__init__(*args, **kwargs)
        self.helper = DefaultFormHelper()
        self.helper.layout = Layout(
            'reddit_username',
            'reddit_password',
            FormActions(
                Submit('save', 'Save', css_class='btn btn-success'),
                Button('cancel', 'Cancel', css_class='btn btn-default', disabled='disabled'),
            ),
        )

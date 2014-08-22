from django.forms.fields import CharField, ChoiceField
from django.forms.forms import Form
from django.forms.widgets import RadioSelect
from praw import Reddit
from verifier.models import Gender


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

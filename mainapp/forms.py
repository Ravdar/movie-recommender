from django import forms
from .models import Feedback

class UserPrompt(forms.Form):
    text = forms.CharField(max_length=2000)
    without_seen = forms.BooleanField(label="Don't already seen", initial=False, required=False)
    only_watchlist = forms.BooleanField(label="Only from watchlist", initial=False, required=False)
    gpt_4= forms.BooleanField(label="GPT-4",initial=False, required=False)

    # I want to pack the attributes below into one, to loop thorugh them in a template
    netflix = forms.BooleanField(label="Netflix",initial=False, required=False)
    amazon_prime = forms.BooleanField(label="Amazon Prime Video", initial=False, required=False)
    disney_plus = forms.BooleanField(label="Disney Plus", initial=False, required=False)
    hulu = forms.BooleanField(label="Hulu", initial=False, required=False)
    hbo_max = forms.BooleanField(label="HBO Max", initial=False, required=False)
    apple_tv = forms.BooleanField(label="Apple TV", initial=False, required=False)
    peacock = forms.BooleanField(label="Peacock", initial=False, required=False)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["category", "mail", "content"]
    


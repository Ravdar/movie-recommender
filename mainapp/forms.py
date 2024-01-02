from django import forms

class UserPrompt(forms.Form):
    text = forms.CharField(max_length=2000)
    gpt_4= forms.BooleanField(label="GPT-4",initial=False)
    #I want to pack the attributes below into one, to loop thorugh them in a template
    netflix = forms.BooleanField(label="Netflix",initial=False)
    amazon_prime = forms.BooleanField(label="Amazon Prime Video", initial=False)
    disney_plus = forms.BooleanField(label="Disney Plus", initial=False)
    hulu = forms.BooleanField(label="Hulu", initial=False)
    hbo_max = forms.BooleanField(label="HBO Max", initial=False)
    apple_tv = forms.BooleanField(label="Apple TV", initial=False)
    peacock = forms.BooleanField(label="Peacock", initial=False)

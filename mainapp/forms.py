from django import forms

class UserPrompt(forms.Form):
    text = forms.CharField(max_length=2000)

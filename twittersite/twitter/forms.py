from django import forms

class PostForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea, max_length=140)
    user = forms.HiddenInput()


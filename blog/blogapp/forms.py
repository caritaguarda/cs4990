from django import forms

class CommentForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'size': 60}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 100}))
    

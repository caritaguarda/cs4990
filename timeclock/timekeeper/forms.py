from django import forms
from .models import Project


class PunchInForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all())



class PunchOutForm(forms.Form):
    note = forms.CharField(max_length=200)






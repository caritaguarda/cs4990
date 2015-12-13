from django import forms

class CreateOpportunityForm(forms.Form):
    contact = forms.ModelForm(queryset='Contact')
    company = forms.ModelForm(queryset='Company', empty_label="None")
    stage = forms.ModelForm(queryset='Stage')
    value = forms.IntegerField()
    source = forms.ModelForm(queryset='Campaign')

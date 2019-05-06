from django import forms
from django.utils import timezone

from .models import mdl_Project, mdl_Task

class form_prj(forms.ModelForm):

    note = forms.CharField(widget=forms.Textarea, required=False) 

    class Meta:
        model = mdl_Project
        fields = ("name", "status", "member", "partner", "note")

class form_tsk(forms.ModelForm):

    note = forms.CharField(widget=forms.Textarea, required=False) 
    
    class Meta:
        model = mdl_Task
        fields = ("project", "name", "status","member", "start", "end", "note")

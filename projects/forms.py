from django import forms
from django.utils import timezone

from .models import mdl_Project, mdl_Task

class form_prj(forms.ModelForm):

    note = forms.CharField(widget=forms.Textarea) 

    class Meta:
        model = mdl_Project
        fields = ("name", "status", "member", "note")

class form_tsk(forms.ModelForm):
    class Meta:
        model = mdl_Task
        fields = ("project", "name", "start", "end")

from django import forms
from .models import Job, JobApplication, Profile

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['resume', 'cover_letter']
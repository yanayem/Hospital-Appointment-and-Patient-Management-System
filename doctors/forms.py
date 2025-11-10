# forms.py
from django import forms
from .models import DoctorProfile

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = [
            'profile_pic', 'specialization', 'highest_qualification', 'license',
            'experience_years', 'expertise_areas', 'specialized_treatments', 'biography'
        ]

from django import forms
from .models import TrackerMaster


class NewComplaintForm(forms.ModelForm):
    class Meta:
        model = TrackerMaster
        fields = ('from_department', 'to_department', 'reason', 'priority')

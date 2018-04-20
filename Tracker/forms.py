from django import forms
from .models import TrackerMaster, ResponseMessage


class NewComplaintForm(forms.ModelForm):
    class Meta:
        model = TrackerMaster
        fields = ('reason', 'priority')


class UserLoginForm(forms.Form):
    user_name = forms.CharField(
        required=True,
        max_length=32
    )

    user_password = forms.CharField(
        required=True,
        max_length=60,
        widget=forms.PasswordInput()
    )


class NewNotification(forms.ModelForm):
    class Meta:
        model = ResponseMessage
        fields = ('message',)

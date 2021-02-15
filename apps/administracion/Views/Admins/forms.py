from django.forms import ModelForm, TextInput, Textarea
from django.contrib.auth.models import User

from apps.administracion.models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'salary',
        ]


class UserFormNew(ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name'
        ]

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'salary',
            'user',
        ]

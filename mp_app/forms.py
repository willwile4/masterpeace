from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TextMP


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    dob = forms.DateField(required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'dob', 'email',
                  'password1', 'password2', )


class CreateTextMPForm(ModelForm):
    class Meta:
        model = TextMP
        fields = ('title', 'text', 'allow_feedback', 'tag', 'artform', )

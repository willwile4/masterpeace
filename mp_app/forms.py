from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False,
                                 help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False,
                                help_text='Optional.')
    date_of_birth = forms.DateField(required=True, help_text='Format: MM/DD/YYYY')
    allow_messages = forms.BooleanField(required=False)
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Something about you...'}),
        max_length=500, required=False)
    facebook_link = forms.URLField(required=False)
    instagram_link = forms.URLField(required=False)
    twitter_link = forms.URLField(required=False)
    email = forms.EmailField(max_length=254, help_text='Required.'
                             'Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'date_of_birth',
                  'allow_messages', 'bio', 'facebook_link', 'instagram_link',
                  'twitter_link', 'email', 'password1', 'password2', )

from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TextMP, UserProfile, ImageMP, ImageTag, Artform, TextMP, TextTag


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    dob = forms.DateField(required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'dob', 'email',
                  'password1', 'password2', )


class EditImage(forms.ModelForm):
    allow_feedback = forms.BooleanField(label='Allow feedback?', required=False)
    title = forms.CharField(max_length=50, required=False)
    caption = forms.CharField(max_length=144, required=False)
    image = forms.ImageField()
    tag = forms.ModelMultipleChoiceField(queryset=ImageTag.objects.all(), required=False)

    class Meta:
        model = ImageMP
        fields = ('allow_feedback', 'title', 'caption', 'image', 'tag', )


class EditText(forms.ModelForm):
    allow_feedback = forms.BooleanField(label='Allow feedback?', required=False)
    title = forms.CharField(max_length=50, required=False)
    text = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}), required=False)
    tag = forms.ModelMultipleChoiceField(queryset=TextTag.objects.all(), required=False)

    class Meta:
        model = TextMP
        fields = ('allow_feedback', 'title', 'text', 'tag', )


class EditProfile(forms.ModelForm):
    pic = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 2.5}), required=False)
    facebook_link = forms.URLField(required=False)
    instagram_link = forms.URLField(required=False)
    twitter_link = forms.URLField(required=False)
    allow_messages = forms.BooleanField(label='Allow messages?', required=False)

    class Meta:
        model = UserProfile
        fields = ('pic', 'bio', 'facebook_link', 'instagram_link',
                  'twitter_link', 'allow_messages')


class CreateTextMPForm(ModelForm):
    class Meta:
        model = TextMP
        fields = ('title', 'text', 'allow_feedback', 'tag', 'artform', )


class DeleteTextMPForm(forms.ModelForm):
    class Meta:
        model = TextMP
        fields = ('title', 'text', 'allow_feedback', 'tag', 'artform')

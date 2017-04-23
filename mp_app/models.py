from django.db import models
from django.contrib.auth.models import User

# default choices
IMG_TYPES = [('PAINT', 'paint'),
             ('DRAW', 'draw'),
             ('SCULPTURE', 'sculpture'),
             ('PHOTO', 'photo'),
             ('MIXED', 'mixed media'),
             ('DIGITAL', 'digital')]

TEXT_TYPES = [('POETRY', 'poetry'),
              ('SHORT STORY', 'short story'),
              ('HUMOR', 'humor'),
              ('ASCII', 'ascii')]


# Create your models here.
class Messages(models.Model):
    message_text = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    has_seen = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to="static/user_images/")
    bio = models.CharField(max_length=500)
    fb_link = models.URLField()
    insta_link = models.URLField()
    twitter_link = models.URLField()
    dob = models.DateField(auto_now_add=False)
    allow_messages = models.BooleanField(default=False)
    followers = models.ManyToManyField('self', symmetrical=False)
    messages = models.ManyToManyField(Messages)


class ImageMP(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    allow_feedback = models.BooleanField(default=False)
    title = models.CharField(max_length=50)
    caption = models.CharField(max_length=144)
    image = models.ImageField(upload_to="static/mp_images/")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    artform = models.CharField(max_length=15, choices=IMG_TYPES)


class TextMP(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    allow_feedback = models.BooleanField(default=False)
    title = models.CharField(max_length=50)
    text = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    artform = models.CharField(max_length=15, choices=TEXT_TYPES)


class ImageFeedback(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    masterpeace = models.ForeignKey(ImageMP, on_delete=models.CASCADE)
    icon = models.CharField(max_length=20)
    has_seen = models.BooleanField


class TextFeedback(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    masterpeace = models.ForeignKey(TextMP, on_delete=models.CASCADE)
    icon = models.CharField(max_length=20)
    has_seen = models.BooleanField()


class ImageTag(models.Model):
    title = models.CharField(max_length=15)
    image = models.ManyToManyField(ImageMP)


class TextTag(models.Model):
    title = models.CharField(max_length=15)
    text = models.ManyToManyField(TextMP)

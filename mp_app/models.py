from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Message(models.Model):
    content = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    from_user = models.ForeignKey(User, related_name='user_from_user')
    to_user = models.ForeignKey(User)

    def __str__(self):
        return self.content[:50]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.FileField(upload_to="masterpeace/static/user_images/",
                            blank=True, null=True)
    bio = models.CharField(max_length=500)
    fb_link = models.URLField(null=True, blank=True)
    insta_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    dob = models.DateField(auto_now_add=False, null=True, blank=True)
    allow_messages = models.BooleanField(default=False)
    followers = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return self.user.username

    # @receiver(post_save, sender=User)
    # def create_profile(sender, instance, created, **kwargs):
    #     if created:
    #         UserProfile.objects.create(user=instance)
    #
    # # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #         instance.UserProfile.save()


class ImageTag(models.Model):
    title = models.CharField(max_length=15)

    def __str__(self):
        return self.title


class TextTag(models.Model):
    title = models.CharField(max_length=15)

    def __str__(self):
        return self.title


class Artform(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class ImageMP(models.Model):
    tag = models.ManyToManyField(ImageTag)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    allow_feedback = models.BooleanField(default=False)
    title = models.CharField(max_length=50)
    caption = models.CharField(max_length=144)
    image = models.FileField(upload_to="masterpeace/static/mp_images/")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    artform = models.ForeignKey(Artform, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class TextMP(models.Model):
    tag = models.ManyToManyField(TextTag)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    allow_feedback = models.BooleanField(default=False)
    title = models.CharField(max_length=50)
    text = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    artform = models.ForeignKey(Artform, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class FeedbackType(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class ImageFeedback(models.Model):
    critic = models.ForeignKey(User, on_delete=models.CASCADE)
    masterpeace = models.ForeignKey(ImageMP, on_delete=models.CASCADE)
    # look into inheritence and polymorphism
    icon = models.ForeignKey(FeedbackType, on_delete=models.CASCADE,
                             null=True, blank=True)
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}, {}'.format(self.critic, self.icon)


class TextFeedback(models.Model):
    critic = models.ForeignKey(User, on_delete=models.CASCADE)
    masterpeace = models.ForeignKey(TextMP, on_delete=models.CASCADE)
    # look into inheritence and polymorphism
    icon = models.ForeignKey(FeedbackType, on_delete=models.CASCADE,
                             null=True, blank=True)
    read = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}, {}'.format(self.critic, self.icon)

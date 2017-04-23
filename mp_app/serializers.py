from rest_framework import Response
from rest_framework import serializers
from .models import UserProfile, Messages, ImageMP, TextMP, ImageFeedback, TextFeedback,
ImageTag, TextTag


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
	           'message_text': {'write_only': True}
                }
        model = Messages
        fields = ('message_text', 'timestamp', 'has_seen')
    # make message_text hidden!


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
	           'dob': {'write_only': True}
               }
        model = UserProfile
        fields = ('username', 'pic', 'bio', 'dob', 'fb_link', 'insta_link',
                  'twitter_link', 'allow_messages', 'followers')


class ImageMPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageMP
        fields = ('owner', 'allow_feedback', 'title', 'caption', 'image', 'created', 'updated', 'artform')


class TextMPSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextMP
        fields = ('owner', 'allow_feedback', 'title', 'text', 'created', 'updated', 'artform')


class ImageFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFeedback
        fields = ('author', 'masterpeace', 'icon', 'has_seen')


class TextFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextFeedback
        fields = ('author', 'masterpeace', 'icon', 'has_seen')


class ImageTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageTag
        fields = ('title', 'image')


class TextTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextTag
        fields = ('title', 'text')

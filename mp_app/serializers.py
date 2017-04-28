from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Message, ImageMP, TextMP, ImageFeedback, TextFeedback, ImageTag, TextTag, Artform


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
                'message_text': {'write_only': True}
                }
        model = Message
        fields = ('content', 'created', 'read', 'to_user', 'from_user')
    # make message_text hidden!


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
    )

    class Meta:
        extra_kwargs = {
                        'dob': {'write_only': True}
                        }
        model = UserProfile
        fields = ('user', 'user_id', 'pic', 'bio', 'dob', 'fb_link', 'insta_link',
                  'twitter_link', 'allow_messages', 'followers')
        read_only_fields = ('pic',)


class ImageMPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageMP
        fields = ('tag', 'owner', 'allow_feedback', 'title', 'caption',
                  'image', 'created', 'updated', 'artform')
        read_only_fields = ('image',)


class TextMPSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextMP
        fields = ('tag', 'owner', 'allow_feedback', 'title', 'text',
                  'created', 'updated', 'artform')


class ImageFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFeedback
        fields = ('critic', 'masterpeace', 'icon', 'read', 'created')


class TextFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextFeedback
        fields = ('critic', 'masterpeace', 'icon', 'read', 'created')


class ImageTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageTag
        fields = ('title',)


class TextTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextTag
        fields = ('title',)


class ArtformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artform
        fields = ('title',)

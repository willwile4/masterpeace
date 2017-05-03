from django.shortcuts import render, redirect
from rest_framework import viewsets
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, CreateTextMPForm
from django.contrib.auth.models import User
from .models import (Message, UserProfile, ImageMP,
                     TextMP, ImageFeedback, TextFeedback,
                     ImageTag, TextTag, Artform)
from .serializers import (UserSerializer, MessageSerializer,
                          UserProfileSerializer,
                          ImageMPSerializer, TextMPSerializer,
                          ImageFeedbackSerializer, TextFeedbackSerializer,
                          ImageTagSerializer, TextTagSerializer,
                          ArtformSerializer)
from django.http import HttpResponseRedirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
import base64
import hashlib
import hmac
import logging
import time
import urllib
from hashlib import sha1
from django.http import HttpResponseRedirect
from django.http import JsonResponse
import os
import json
import boto3

logger = logging.getLogger(__name__)


def index(request):
    image_mps = ImageMP.objects.all().order_by('-created')
    text_mps = TextMP.objects.all().order_by('-created')
    user_profiles = UserProfile.objects.all()
    return render(request, 'mp_app/index.html', {
                                           'image_mps': image_mps,
                                           'text_mps': text_mps,
                                           'user_profiles': user_profiles})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/profile/{}'.format(user.id))
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def profile(request, user_id):
    if len(UserProfile.objects.filter(user_id=user_id)) > 0:
        user_profile = UserProfile.objects.get(user_id=user_id)
        user = User.objects.get(id=user_id)
        image_mps = ImageMP.objects.filter(owner_id=user.id).order_by('-created')
        text_mps = TextMP.objects.filter(owner_id=user.id).order_by('-created')
        return render(request, 'mp_app/profile.html', {'profile': user_profile,
                                                       'image_mps': image_mps,
                                                       'text_mps': text_mps})
    else:
        user = User.objects.get(id=user_id)
        return render(request, 'mp_app/create_profile.html', {'user': user})


def create_textMP(request, user_id):
    if request.method == 'POST':
        f = CreateTextMPForm(request.POST)
        if f.is_valid():
            owner = User.objects.get(pk=request.user.id)
            title = f.cleaned_data.get('title')
            text = f.cleaned_data.get('text')
            allow_feedback = f.cleaned_data.get('allow_feedback')
            artform = f.cleaned_data.get('artform')

            textMP = TextMP(owner=owner, title=title, text=text,
                            allow_feedback=allow_feedback, artform=artform)
            textMP.save()
            return redirect('/')

    else:
        user = User.objects.get(id=user_id)
        info = user.__dict__
        return render(request, 'mp_app/create_profile.html', info)


def privacy(request):
    return render(request, 'mp_app/privacypolicy.html')


def account(request):
    return render(request, 'mp_app/s3_test.html')


def blob_test(request):
    return render(request, 'mp_app/blob_test.html')

def sign_s3(request):
    pass
#     # AWS_ACCESS_KEY = os.environ.get('AWSAccessKeyId')
#     AWS_ACCESS_KEY = 'AKIAIM26OJZRVLFHUENQ'
#     AWS_SECRET_KEY = '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'
#     S3_BUCKET = 'masterpeace'
#     # file_name = request.GET.get('file_name')
#     # file_type = request.GET.get('file_type')
#
#     object_name = urllib.parse.quote_plus(request.GET['file_name'])
#     mime_type = request.GET['file_type']
#     print(object_name, mime_type)
#
#     # s3_resource = boto3.resource('s3')
#     # s3 = s3_resource.meta.client
#
#     secondsPerDay = 36000
#     expires = int(time.time()+secondsPerDay)
#     amz_headers = "x-amz-acl:public-read"
#
#     string_to_sign = "POST\n\n{}\n{}\n{}\n/{}/{}".format(mime_type, expires,
#                                                     amz_headers, S3_BUCKET,
#                                                     object_name)
#
#     encodedSecretKey = AWS_SECRET_KEY.encode()
#
#     encodedString = string_to_sign.encode()
#     h = hmac.new(encodedSecretKey, encodedString, sha1)
#     hDigest = h.digest()
#     signature = base64.encodebytes(hDigest).strip()
#     signature = urllib.parse.quote_plus(signature)
#     url = 'https://{}.s3.amazonaws.com/{}'.format(S3_BUCKET, object_name)
#
#     return JsonResponse({
#         'signed_request': '{}?AWSAccessKeyId={}&Expires={}&Signature=%{}'.format(url,
#                                             AWS_ACCESS_KEY, expires, signature),
#         'url': url,
#     })

    # presigned_post = s3.generate_presigned_post(
    #     Bucket='masterpeace',
    #     Key=file_name,
    #     Fields={'acl': "public-read", "Content-Type": file_type},
    #     Conditions=[
    #         {'acl': 'public-read'},
    #         {'Content-Type': file_type}
    #     ],
    #     ExpiresIn=3600,
    #     # AWS_access_key=os.environ.get('AWS_ACCESS_KEY_ID'),
    #     # AWS_secret_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    # )
    # print(presigned_post)
    # return json.dumps({
    #     'data': presigned_post,
    #     'url': 'https://{}.s3.amazonaws.com/{}'.format(S3_BUCKET, file_name)
    # })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def sign_s3(self, request):
        S3_BUCKET = os.environ.get('S3_BUCKET')

        file_name = request.args.get('file_name')
        file_type = request.args.get('file_type')

        s3 = boto3.client('s3')

        presigned_post = s3.generate_presigned_post(
            Bucket=S3_BUCKET,
            Key=file_name,
            Fields={'acl': "public-read", "Content-Type": file_type},
            Conditions=[
                {'acl': 'public-read'},
                {'Content-Type': file_type}
            ],
            ExpiresIn=3600
        )

        return json.dumps({
            'data': presigned_post,
            'url': 'https://{}.s3.amazonaws.com/{}'.format(S3_BUCKET, file_name)
        })

    def submit_form(self, request):
        if request.method == 'POST':
            user_id = request.form['user_id']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            password = request.form['password']
            confirm_password = request.form['conf_password']
            email = request.form['email']
            avatar_url = request.form['avatar-url']
            dob = request.form['DOB']
            bio = request.form['bio']
            fb = request.form['FBlink']
            insta = request.form['Instalink']
            twitter = request.form['Twitterlink']
            allow_messages = request.form['allow_messages']

            u = UserProfile(user_id, first_name, last_name, password,
                            confirm_password, email, avatar_url, dob, bio, fb,
                            insta, twitter, allow_messages)
            print("cool")
            u.save()

        return HttpResponseRedirect('/profile/')


class ImageMPViewSet(viewsets.ModelViewSet):
    queryset = ImageMP.objects.all()
    serializer_class = ImageMPSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (FormParser, MultiPartParser)

    def sign_s3(self, request):
        S3_BUCKET = os.environ.get('S3_BUCKET')

        file_name = request.args.get('file_name')
        file_type = request.args.get('file_type')

        s3 = boto3.client('s3')

        presigned_post = s3.generate_presigned_post(
            Bucket=S3_BUCKET,
            Key=file_name,
            Fields={'acl': "public-read", "Content-Type": file_type},
            Conditions=[
                {'acl': 'public-read'},
                {'Content-Type': file_type}
            ],
            ExpiresIn=3600
        )

        return json.dumps({
            'data': presigned_post,
            'url': 'https://{}.s3.amazonaws.com/{}'.format(S3_BUCKET, file_name)
        })

    def submit_form(self, request):
        if request.method == 'POST':
            pass

        #     self.update(username, first_name, last_name, password,
        #                 confirm_password, email, avatar_url, dob, bio, fb,
        #                 insta, twitter, allow_messages)
        #
        # return HttpResponseRedirect('/profile/')


class TextMPViewSet(viewsets.ModelViewSet):
    queryset = TextMP.objects.all()
    serializer_class = TextMPSerializer


class ImageFeedbackViewSet(viewsets.ModelViewSet):
    queryset = ImageFeedback.objects.all()
    serializer_class = ImageFeedbackSerializer


class TextFeedbackViewSet(viewsets.ModelViewSet):
    queryset = TextFeedback.objects.all()
    serializer_class = TextFeedbackSerializer


class ImageTagViewSet(viewsets.ModelViewSet):
    queryset = ImageTag.objects.all()
    serializer_class = ImageTagSerializer


class TextTagViewSet(viewsets.ModelViewSet):
    queryset = TextTag.objects.all()
    serializer_class = TextTagSerializer


class ArtformViewSet(viewsets.ModelViewSet):
    queryset = Artform.objects.all()
    serializer_class = ArtformSerializer

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
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from django.db.models import Q
import os
import json
import boto3


def index(request):
    image_mps = ImageMP.objects.all().order_by('-created')
    text_mps = TextMP.objects.all().order_by('-created')
    user_profiles = UserProfile.objects.all()
    u_m = len(Message.objects.filter(to_user_id=request.user.id, read=False))
    return render(request, 'mp_app/index.html', {
                                           'image_mps': image_mps,
                                           'text_mps': text_mps,
                                           'user_profiles': user_profiles,
                                           'unread_messages': u_m})


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
    messages = Message.objects.filter(to_user_id=request.user.id, read=False)
    u_m = len(messages)
    if UserProfile.objects.filter(user_id=user_id).exists():
        user_profile = UserProfile.objects.get(user_id=user_id)
        user = User.objects.get(id=user_id)
        image_mps = ImageMP.objects.filter(owner_id=user.id).order_by('-created')
        text_mps = TextMP.objects.filter(owner_id=user.id).order_by('-created')
        return render(request, 'mp_app/profile.html', {'profile': user_profile,
                                                       'image_mps': image_mps,
                                                       'text_mps': text_mps,
                                                       'unread_messages': u_m})
    else:
        user = User.objects.get(id=user_id)
        return render(request, 'mp_app/create_profile.html', {'user': user})


class Conversation:
    def __init__(self, user_id, other):
        self.id = user_id
        self.other = other
        self.messages = [message for message in Message.objects.filter(Q(from_user_id=other.id, to_user_id=user_id) | Q(to_user_id=other.id, from_user_id=user_id)).order_by('created')]
        self.unread = Message.objects.filter(to_user_id=user_id, from_user_id=other.id, read=False).exists()
        self.latest_message = self.messages[-1]


def messages(request):
    convo_users = [User.objects.get(id=user_id) for user_id in set([message.to_user_id if message.from_user_id == request.user.id else message.from_user_id for message in Message.objects.filter(Q(from_user_id=request.user.id) | Q(to_user_id=request.user.id))])]
    conversations = [Conversation(request.user.id, user) for user in convo_users][::-1]
    # all_messages = Message.objects.filter(to_user_id=request.user.id)
    last_messages = (Message.objects.filter(from_user_id=user.id).order_by('created')[0] for user in convo_users)
    unread_messages = Message.objects.filter(to_user_id=request.user.id,
                                             read=False)
    u_m = len(unread_messages)
    return render(request, 'mp_app/messages.html', {
                                                    # 'messages': all_messages,
                                                    'unread_messages': u_m,
                                                    'last_messages': last_messages,
                                                    'convos': conversations})


def message_detail(request, user_id):
    messages = Message.objects.filter(Q(from_user_id=user_id, to_user_id=request.user.id) | Q(to_user_id=user_id, from_user_id=request.user.id)).order_by('created')
    for message in messages:
        message.read = True
        message.save()
    u_m = len(Message.objects.filter(to_user_id=request.user.id, read=False))
    return render(request, 'mp_app/message_detail.html',
                  {'unread_messages': u_m,
                   'messages': messages,
                   'user': User.objects.get(id=user_id)})


def create_textMP(request):
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

# def create_textMP(request):
#     if request.method == 'POST':
#         f = CreateTextMPForm(request.POST)
#         if f.is_valid():
#             owner = User.objects.get(pk=request.user.id)
#             title = f.cleaned_data.get('title')
#             text = f.cleaned_data.get('text')
#             allow_feedback = f.cleaned_data.get('allow_feedback')
#             artform = f.cleaned_data.get('artform')
#
#             textMP = TextMP(owner=owner, title=title, text=text,
#                             allow_feedback=allow_feedback, artform=artform)
#             textMP.save()
#             #
#             # tag = [t for t in f.cleaned_data.get('tag')]
#             # print(tag, type(tag))
#             # for t in tag:
#             #     t.save()
#             #
#             # textMP.tag.copy(tag)
#             # textMP.save()
#             return redirect('/')
#     else:
#         f = CreateTextMPForm()
#     return render(request, 'mp_app/create.html', {'form': f})


def privacy(request):
    return render(request, 'mp_app/privacypolicy.html')


def account(request):
    return render(request, 'mp_app/account.html')


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

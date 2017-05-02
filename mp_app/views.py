from django.http import Http404
from django.shortcuts import render, redirect
from rest_framework import viewsets
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, CreateTextMPForm, EditProfile, EditImage, EditText
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
from django.db.models import Q
import os
import json
import boto3


def mp_jumblr():
    '''
    Combines posts into one queryset to render on templates.
    '''
    textmps = [(mp, mp.created) for mp in TextMP.objects.all()]
    imagemps = [(mp, mp.created) for mp in ImageMP.objects.all()]
    allmps = reversed(sorted(textmps + imagemps, key=lambda mp: mp[1]))
    return ([item[0] for item in allmps])


def index(request):
    all_mps = mp_jumblr()
    user_profiles = UserProfile.objects.all()
    messages = Message.objects.filter(to_user_id=request.user.id, read=False)
    u_m = len(messages)
    return render(request, 'mp_app/index.html', {
                                           'all_mps': all_mps,
                                           'user_profiles': user_profiles,
                                           'messages': messages,
                                           'unread_messages': u_m})


def profile(request, user_id):
    if UserProfile.objects.filter(user_id=user_id).exists():
        messages = Message.objects.filter(to_user_id=request.user.id, read=False)
        u_m = len(messages)
        user_profile = UserProfile.objects.get(user_id=user_id)
        user = User.objects.get(id=user_id)
        all_mps = mp_jumblr()
        return render(request, 'mp_app/profile.html', {'profile': user_profile,
                                                       'all_mps': all_mps,
                                                       'unread_messages': u_m})
    elif request.user.id == user_id:
        user = User.objects.get(id=user_id)
        return render(request, 'mp_app/create_profile.html', {'user': user})


def edit_profile(request):
    user = request.user
    try:
        profile = UserProfile.objects.get(user_id=user.id)
    except UserProfile.DoesNotExist:
        raise Http404("Profile does not exist")

    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            profile.pic = profile.pic
            profile = form.save(commit=True)
            profile.save()
            return redirect('/profile/{}'.format(user.id), pk=profile.pk)

    else:
        form = EditProfile(instance=profile)
    return render(request, 'mp_app/edit_profile.html', {'form': form,
                                                        'profile': profile})


def edit_image(request, id):
    user = request.user
    try:
        image = ImageMP.objects.get(id=id)
    except ImageMP.DoesNotExist:
        raise Http404("Image does not exist")

    if request.method == 'POST':
        form = EditImage(request.POST, request.FILES, instance=image)

        if form.is_valid():
            image = form.save(commit=True)
            image.save()
            return redirect('/profile/{}'.format(user.id), pk=image.pk)

    else:
        form = EditImage(instance=image)
    return render(request, 'mp_app/edit_image.html', {'form': form,
                                                      'image': image})


def edit_text(request, id):
    user = request.user
    try:
        text = TextMP.objects.get(id=id)
    except TextMP.DoesNotExist:
        raise Http404("Image does not exist")

    if request.method == 'POST':
        form = EditText(request.POST, request.FILES, instance=text)

        if form.is_valid():
            text = form.save(commit=True)
            text.save()
            return redirect('/profile/{}'.format(user.id), pk=text.pk)

    else:
        form = EditText(instance=text)
    return render(request, 'mp_app/edit_text.html', {'form': form,
                                                     'text': text})


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


class Conversation:
    def __init__(self, user_id, other):
        self.id = user_id
        self.other = other
        self.messages = [message for message in Message.objects.filter(Q(from_user_id=other.id, to_user_id=user_id) | Q(to_user_id=other.id, from_user_id=user_id)).order_by('created')]
        self.unread = Message.objects.filter(to_user_id=user_id, from_user_id=other.id, read=False).exists()
        if self.messages:
            self.latest_message = self.messages[-1]


def messages(request):
    convo_users = [User.objects.get(id=user_id) for user_id in set([message.to_user_id if message.from_user_id == request.user.id else message.from_user_id for message in Message.objects.filter(Q(from_user_id=request.user.id) | Q(to_user_id=request.user.id))])]
    conversations = sorted([Conversation(request.user.id, user) for user in convo_users], key=lambda conversation: conversation.latest_message.created)[::-1]
    unread_messages = Message.objects.filter(to_user_id=request.user.id,
                                             read=False)
    u_m = len(unread_messages)
    return render(request, 'mp_app/messages.html', {'unread_messages': u_m,
                                                    'convos': conversations})


def message_detail(request, user_id):
    conversation = Conversation(request.user.id, User.objects.get(id=user_id))
    for message in conversation.messages:
        if message.to_user_id == request.user.id:
            message.read = True
            message.save()
    u_m = len(Message.objects.filter(to_user_id=request.user.id, read=False))
    other_user = User.objects.get(id=user_id)
    context = {'unread_messages': u_m,
     'conversation': conversation,
     'other_user': other_user,
     'user': request.user}
    if UserProfile.objects.filter(user_id=user_id).exists():
        context['profile'] = UserProfile.objects.get(user_id=user_id)
    return render(request, 'mp_app/message_detail.html', context)


def create_textMP(request):
    if request.method == 'POST':
        f = CreateTextMPForm(request.POST)
        if f.is_valid():
            textMP = f.save(commit=False)
            textMP.owner = User.objects.get(pk=request.user.id)
            textMP.title = f.cleaned_data.get('title')
            textMP.text = f.cleaned_data.get('text')
            textMP.allow_feedback = f.cleaned_data.get('allow_feedback')
            textMP.artform = f.cleaned_data.get('artform')
            textMP.save()
            textMP.tag = f.cleaned_data.get('tag')
            f.save_m2m()
            return redirect('/')
    else:
        f = CreateTextMPForm()
    return render(request, 'mp_app/create.html', {'form': f})


def filter_text_tags(request, tag_id):
    texttags = TextTag.objects.filter(id=tag_id)
    context = {'texttags': texttags}
    return render(request, 'mp_app/filter_text_tags.html', context)


def filter_image_tags(request, tag_id):
    imagetags = ImageTag.objects.filter(id=tag_id)
    context = {'imagetags': imagetags}
    return render(request, 'mp_app/filter_image_tags.html', context)


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

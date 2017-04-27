from django.shortcuts import render, redirect
from rest_framework import viewsets
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, CreateTextMPForm
from django.contrib.auth.models import User
from .models import (Message, UserProfile, ImageMP,
                     TextMP, ImageFeedback, TextFeedback,
                     ImageTag, TextTag, Artform)
from .serializers import (MessageSerializer, UserProfileSerializer,
                          ImageMPSerializer, TextMPSerializer,
                          ImageFeedbackSerializer, TextFeedbackSerializer,
                          ImageTagSerializer, TextTagSerializer,
                          ArtformSerializer)


def index(request):
    return render(request, 'mp_app/index.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def profile(request, profile_id):
    user_profile = UserProfile.objects.get(id=profile_id)
    info = user_profile.__dict__
    user = User.objects.get(id=user_profile.user_id)
    info['username'] = user.username
    info['first_name'] = user.first_name
    info['last_name'] = user.last_name
    info['email'] = user.email
    info['date_joined'] = user.date_joined
    return render(request, 'mp_app/profile.html', {'profile': info})


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
            # 
            # tag = [t for t in f.cleaned_data.get('tag')]
            # print('coastal elite', tag, type(tag))
            # for t in tag:
            #     t.save()
            #
            # textMP.tag.copy(tag)
            # textMP.save()
            return redirect('/')
    else:
        f = CreateTextMPForm()
    return render(request, 'mp_app/create.html', {'form': f})


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class ImageMPViewSet(viewsets.ModelViewSet):
    queryset = ImageMP.objects.all()
    serializer_class = ImageMPSerializer


class TextMPViewSet(viewsets.ModelViewSet):
    queryset = TextMP.objects.all()
    serializer_class = TextMPSerializer

    # def create(self, request):
    #     if self.request.method == 'POST':
    #         f = CreateTextMPForm(request.POST)
    #         if f.is_valid():
    #             f = f.cleaned_data()
    #             f.save()
    #             return redirect('/')
    #     else:
    #         f = CreateTextMPForm()
    #     return render(request, 'mp_app/create.html', {'form': f})


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

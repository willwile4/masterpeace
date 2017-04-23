"""masterpeace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from mp_app import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'message', views.MessageViewSet)
router.register(r'profile', views.UserProfileViewSet)
router.register(r'image_mp', views.ImageMPViewSet)
router.register(r'text_mp', views.TextMPViewSet)
router.register(r'image_feedback', views.ImageFeedbackViewSet)
router.register(r'text_feedback', views.TextFeedbackViewSet)
router.register(r'image_tag', views.ImageTagViewSet)
router.register(r'text_tag', views.TextTagViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.index, name="index"),
    url(r'^admin/', admin.site.urls),
]

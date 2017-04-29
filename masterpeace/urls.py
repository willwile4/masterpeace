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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from mp_app import views
from rest_framework import routers
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
# router.register(r'message', views.MessageViewSet)
router.register(r'profile', views.UserProfileViewSet)
router.register(r'image_mp', views.ImageMPViewSet)
router.register(r'text_mp', views.TextMPViewSet)
router.register(r'image_feedback', views.ImageFeedbackViewSet)
router.register(r'text_feedback', views.TextFeedbackViewSet)
router.register(r'image_tag', views.ImageTagViewSet)
router.register(r'text_tag', views.TextTagViewSet)
router.register(r'artform', views.ArtformViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),
    url(r'^$', include('mp_app.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r"^soc/", include("social_django.urls", namespace="social")),
    url(r'^profile/(?P<user_id>[0-9]+)', views.profile, name='profile'),
    url(r'^edit_profile/', views.edit_profile, name="edit_profile"),
    url(r'^privacy/', views.privacy, name="privacy"),
    url(r'^account/', views.account, name='account'),
    url(r'^create_textMP/$', views.create_textMP, name='create_textMP'),
    url(r'^messages/$', views.messages, name='messages'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

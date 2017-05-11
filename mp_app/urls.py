from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/(?P<user_id>[0-9]+)', views.profile, name='profile'),
    url(r'^edit_profile/', views.edit_profile, name="edit_profile"),
    url(r'^edit_image/(?P<id>[0-9]+)', views.edit_image, name="edit_image"),
    url(r'^edit_text/(?P<id>[0-9]+)', views.edit_text, name="edit_text"),
    url(r'^privacy/', views.privacy, name="privacy"),
    url(r'^create_textMP/$', views.create_textMP, name='create_textMP'),
    url(r'^messages/$', views.messages, name='messages'),
    url(r'^messages/(?P<user_id>[0-9]+)',
        views.message_detail, name='message_detail'),
    url(r'^text_tags/(?P<tag_id>[0-9]+)',
        views.filter_text_tags, name='filter_text_tags'),
    url(r'^image_tags/(?P<tag_id>[0-9]+)',
        views.filter_image_tags, name='filter_image_tags'),
    url(r'^blob_test', views.blob_test, name='blob_test'),
    url(r'^create_image', views.create_image, name='create_image'),
    url(r'^about', views.about, name='about'),
]

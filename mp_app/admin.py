from django.contrib import admin
from .models import (UserProfile, Message, ImageMP,
                     TextMP, ImageFeedback, TextFeedback,
                     ImageTag, TextTag, Artform, FeedbackType)

admin.site.register(Message)
admin.site.register(UserProfile)
admin.site.register(ImageMP)
admin.site.register(TextMP)
admin.site.register(ImageFeedback)
admin.site.register(TextFeedback)
admin.site.register(ImageTag)
admin.site.register(TextTag)
admin.site.register(Artform)
admin.site.register(FeedbackType)

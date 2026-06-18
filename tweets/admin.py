from django.contrib import admin
from .models import Tweet, Like, Follow

admin.site.register(Tweet)
admin.site.register(Like)
admin.site.register(Follow)

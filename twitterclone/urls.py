from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path("tweets/",include("tweets.urls")),
    path("admin/", admin.site.urls),
]

from django.contrib import admin
from django.urls import path, include
from tweets import views as tweets_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path("accounts/register/", tweets_views.register, name="regster"),
    path("", include("tweets.urls"),)
]

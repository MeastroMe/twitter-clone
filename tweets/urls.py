from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("feed/", views.feed, name="feed"),
    path("posts/", views.post_tweet, name="post_tweet"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("like/<int:tweet_id>/", views.toggle_like, name="toggle_like"),
    path("follow/<str:username>/", views.toggle_follow, name="toggle_follow"),
    path("search/", views.search_users, name="search_users"),

]   
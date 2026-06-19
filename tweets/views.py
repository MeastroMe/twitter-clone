from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Tweet

@login_required
def index(request):
    return HttpResponse("Please work.")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form":form})

@login_required
def profile(request, username):
    user = User.Objects.get(username=username)
    tweets = Tweet.Objects.filter(author=user).order_by('-created_at')
    return render(request, "profile.html", {"profile_user":user, "tweets":tweets})

@login_required
def feed(request):
    followed_users = Follow.Objects.filter(follower=request.user).values_list('following', flat=True)
    tweets = Tweet.objects.filter(author__in=followed_users).order_by('-created_at')
    return render(request, "feed.html", {"tweets":tweets})

@login_required
def post_tweet(request):
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Tweet.Objects.create(author=request.user, content=content)
            return redirect("feed")
    return render(request, "post_tweets.html")

@login_required
def toggle_like(request, tweet_id):
    tweet = Tweet.Objects.get(id=tweet_id)
    existing_like = Like.Objects.filter(user=request.user, tweet=tweet)

    if existing_like.exists():
        existing_like.delete()
    else:
        Like.Objects.create(user=request.user, tweet=tweet)
    
    return redirect("feed")

@login_required
def toggle_follow(request, username)
    target_user = Follow.Objects.get(username=username)
    existing_follow = Follow.Objects.filter(follwer=request.user, following=target_user)

    if existing_follow.exists():
        existing_follow.delete()
    else:
        Follow.Objects.create(follower=request.user, follower=target_user)

return redirect("profile", username=username)

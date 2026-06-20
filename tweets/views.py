from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .models import Tweet, Like, Follow

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
    user = User.objects.get(username=username)
    tweets = Tweet.objects.filter(author=user).order_by('-created_at')
    return render(request, "profile.html", {"profile_user":user, "tweets":tweets})

@login_required
def feed(request):
    followed_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    tweets = Tweet.objects.filter(author__in=followed_users).order_by('-created_at')

    liked_tweet_ids = Like.objects.filter(user=request.user).values_list('tweet_id', flat=True)
    return render(request, "feed.html", {"tweets":tweets, "liked_tweet_ids": liked_tweet_ids})

@login_required
def post_tweet(request):
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Tweet.objects.create(author=request.user, content=content)
            return redirect("feed")
    return render(request, "post_tweet.html")

@login_required
@require_POST
def toggle_like(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    existing_like = Like.objects.filter(user=request.user, tweet=tweet)

    if existing_like.exists():
        existing_like.delete()
    else:
        Like.objects.create(user=request.user, tweet=tweet)
    
    return redirect("feed")

@login_required
@require_POST
def toggle_follow(request, username):
    target_user = User.objects.get(username=username)
    existing_follow = Follow.objects.filter(follower=request.user, following=target_user)

    if existing_follow.exists():
        existing_follow.delete()
    else:
        Follow.objects.create(follower=request.user, following=target_user)

    return redirect("profile", username=username)

@login_required
def search_users(request):
    query = request.GET.get("q", "")
    results = User.objects.filter(username__icontains=query) if query else []
    return render(request, "search.html", {"results": results, "query": query})
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
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
def feed(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, "feed.html", {"tweets":tweets})
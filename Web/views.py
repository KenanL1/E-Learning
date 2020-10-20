from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms

from .models import User


# Create your views here.
def index(request):
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "Web/learn.html")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

def login_view(request):
        return render(request, "Web/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
        return render(request, "Web/register.html")

@login_required
def forum(request):
    return render(request, "Web/forum.html")

@login_required
def quiz(request):
    return render(request, "Web/quiz.html")

def solution(request):
    return render(request, "Web/solution.html")

def about(request):
    return render(request, "Web/about.html")

def contact(request):
    return render(request, "Web/contact.html")

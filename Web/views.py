from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm

# Login
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.decorators import login_required  # decorator

# Create your views here.
def index(request):
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "Web/learn.html")

    # Everyone else is prompted to sign in
    else:
        return render(request, "Web/index.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()  # saving to db
            user.set_password(user.password)  # setting up hash
            user.save()

            # website profile pic
            profile = profile_form.save(commit=False)
            profile.user = user  # sets up one to one relationship

            # check if profile pic was uploaded/can be used to upload pdf, resumes and other stuff also "request.FILES"
            if "profile_pic" in request.FILES:
                profile.profile_pic = request.FILES["profile_pic"]

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(
        request,
        "Web/register.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "registered": registered,
        },
    )

# dont name your view login, youre importing a login module.. will mess up code
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # django authentication system
        user = authenticate(username=username, password=password)  # authenticate user

        if user:
            if user.is_active:
                login(request, user)  # login user in
                return HttpResponseRedirect(
                    reverse("index")
                )  # bring user to home page after login

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone treid to login and failed!")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("invalid login details supplied!")

    else:
        return render(request, "Web/login.html", {})


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

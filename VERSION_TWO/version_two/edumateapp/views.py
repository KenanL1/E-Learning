from django.shortcuts import render
from django.http import HttpResponse
from edumateapp.forms import UserForm, UserProfileInfoForm

# Login
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.decorators import login_required  # decorator

# Create your views here.

# main page
def index(request):
    return render(request, "edumate/index.html")


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
        "edumate/registeration.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "registered": registered,
        },
    )


# dont name your view login, youre importing a login module.. will mess up code
def user_login(request):
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
        return render(request, "edumate/login.html", {})


# login required decorator used
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

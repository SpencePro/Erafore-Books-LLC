from django.contrib import auth
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django import forms

from usersapp.models import User, Follow, Wish
from mainapp.models import Book, Series


def login(request):
    # GET request loads page, POST request submits
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            return HttpResponseRedirect(reverse("index"))
        else:
            context = {
                "message": "Invalid login credentials",
            }
            return render(request, "login.html", context)
    else:
        return render(request, "login.html")


def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    # GET request loads page, POST request submits
    error_message = ""

    if request.method == "POST":    
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # check length of password/username
        if len(username) < 6:
            error_message = "Invalid username"
            return render(request, "register.html", context={"error_message": error_message})
        elif len(password) < 8:
            error_message = "Invalid password"
            return render(request, "register.html", context={"error_message": error_message})
        
        # password must match confirmation
        if password != confirmation:
            error_message = "Password and confirmation do not match"
            return render(request, "register.html", context={"error_message": error_message})

        # password must contain at least 1 special character, 1 number and 1 capital letter
        upper_count = 0
        special_count = 0
        num_count = 0

        for character in password:
            if character.isupper():
                upper_count+=1
            elif not character.isalnum():
                special_count += 1
            elif character.isdigit():
                num_count += 1

        if upper_count == 0 or num_count == 0 or special_count == 0:
            error_message = "Invalid password"
            return render(request, "register.html", context={"error_message": error_message})
        
        # username must be unique
        try_user = User.objects.get(username=username)
        if not try_user:
            error_message = "Invalid username"
            return render(request, "register.html", context={"error_message": error_message})

        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "register.html", context={"error_message": error_message})


# need to use with EmailApp; re-think this one
@login_required(login_url="login")
def reset_password(request, id):
    # POST request
    if request.method == "POST":
        current_password = request.POST["current-password"]
        new_password = request.POST["new-password"]
        username = request.user.username
        user = authenticate(request, username=username, password=current_password)
        
        if user is not None:
            pass

    return HttpResponseRedirect(reverse("profile", kwargs={"username": request.user.username}))


@login_required(login_url="login")
def delete_account(request, id):
    # POST request
    # use AJAX
    if request.method == "POST":
        password = request.POST["password"]
        authenticated = authenticate(request, username=request.user.username, password=password)
        if authenticated is not None:
            user = User.objects.get(pk=id)
            user.delete()
            return HttpResponseRedirect(reverse("logout"))
        else:
            return HttpResponseRedirect(reverse("profile", kwargs={"username": request.user.username}))


'''def change_email(request, id):
    # POST request
    # use AJAX
    if request.method == "POST":
        user = User
    return HttpResponseRedirect(reverse("profile", kwargs={"username": request.user.username}))'''


@login_required(login_url="login")
def edit_settings(request):
    # POST request
    # use AJAX
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        sales = request.POST["sales"]
        updates = request.POST["follow-updates"]

        if sales == "":
            user.can_send_sales = False
        if updates == "":
            user.can_send_updates = False
        user.save()

    return HttpResponseRedirect(reverse("profile", kwargs={"username": user}))


@login_required(login_url="login")
def profile_view(request, username):
    # GET request views page, display username, email address on file (if user == user accessing), wishlist + following
    current_user = User.objects.get(username=username)
    wishlist = Wish.objects.filter(user=username)
    series_followed = Follow.objects.filter(follower=username)

    context = {
        "current_user": current_user,
        "wishlist": wishlist,
        "series_followed": series_followed,
    }
    return render(request, "profile.html", context)


@login_required(login_url="login")
def add_to_wishlist(request, id):
    # POST request
    # update with AJAX
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        book = Book.objects.get(pk=id)

        try_wish = Wish.objects.filter(user=user, book=book)
        if try_wish.exists():
            try_wish.delete()
            result = "removed"
        else:
            add_wish = Wish(user=user, book=book)
            add_wish.save()
            result = "added"
        
    context = {
        "result": result
    }
    return render(request, "profile.html", context)


@login_required(login_url="login")
def follow_series(request, id):
    # POST request
    # update with AJAX
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        series = Series.objects.get(pk=id)
        
        try_follow = Follow.objects.filter(follower=user, series=series)
        if try_follow.exists():
            try_follow.delete()
            result = "removed"
        else:
            follow = Follow(follower=user, series=series)
            follow.save()
            result = "added"

    context = {
        "result": result
    }
    return render(request, "profile.html", context)


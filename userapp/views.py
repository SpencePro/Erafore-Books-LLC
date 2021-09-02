from django.contrib import auth
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
import random

from userapp.models import User, Follow, Wish
from mainapp.models import Book, Series
from emailapp.views import verify_account, change_password
from userapp.validators import validate_pword


def login_view(request):
    # GET request loads page, POST request submits
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"success": True, "url": reverse("index")})
        else:
            return JsonResponse({"success": False, "message": "Invalid login credentials"})
    else:
        return render(request, "login.html")


@login_required(login_url="login")
def logout_confirm_view(request):
    return render(request, "logout_confirm.html")


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    # GET request loads page, POST request submits
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # check length of username
        if len(username) < 6:
            error_message = "Invalid username"
            return JsonResponse({"success": False, "error_message": error_message}) 

        # validate password
        validate = validate_pword(password, confirmation, username, email)
        if validate != None:
            return JsonResponse({"success": False, "error_message": validate})

        # username must be unique
        try_user = User.objects.filter(username=username)
        if len(try_user) > 0:
            error_message = "Invalid username"
            return JsonResponse({"success": False, "error_message": error_message})
        else:
            # send email to user with code, if they enter code successfully, activate account
            passcode = random.randint(100000, 1000000)
            verify_account(email, passcode)
            request.session["passcode"] = passcode
            request.session["username"] = username
            request.session["email"] = email
            request.session["password"] = password
            return JsonResponse({"success": True, "url": reverse("verify_registration")})
    else:
        return render(request, "register.html")


def verify_registration(request):
    if request.method == "POST":
        user_submission = int(request.POST["passcode"])
        passcode = int(request.session["passcode"])
        username = request.session["username"]
        email = request.session["email"]
        password = request.session["password"]
        
        if user_submission == passcode:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            del request.session["passcode"]
            del request.session["username"]
            del request.session["email"]
            del request.session["password"]
            return JsonResponse({"success": True, "url": reverse("login")})
        else:
            error_message = "Incorrect Passcode"
            del request.session["passcode"]
            del request.session["username"]
            del request.session["email"]
            del request.session["password"]
            return JsonResponse({"success": False, "error_message": error_message, "url": reverse("register")})
    else:
        return render(request, "verify_email.html")


# reset user's password if they forget it
def reset_password(request):
    if request.method == "POST":
        username = request.POST["reset-username"]
        email = request.POST["email"]
        
        user = User.objects.filter(username=username, email=email)
        if len(user) < 1:
            return JsonResponse({"success": False, "error_message": "Invalid credentials"})
        else:
            passcode = random.randint(100000, 1000000)
            change_password(email, passcode)
            request.session["passcode"] = passcode
            request.session["username"] = username
            request.session["email"] = email
            return JsonResponse({"success": True, "url": reverse("verify_reset")})


def verify_reset(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        user_submission = int(request.POST["passcode"])
        passcode = int(request.session["passcode"])
        username = request.session["username"]
        email = request.session["email"]

        validate = validate_pword(password, confirmation, username, email)
        if validate != None:
            return JsonResponse({"success": False, "error_message": validate})

        # Verify user's passcode
        if user_submission == passcode:
            user = User.objects.get(username=username, email=email)
            new_password = make_password(password)
            user.password = new_password
            user.save()
            del request.session["passcode"]
            del request.session["username"]
            del request.session["email"]
            return JsonResponse({"success": True, "url": reverse("login")})
        else:
            error_message = "Incorrect Passcode"
            del request.session["passcode"]
            del request.session["username"]
            del request.session["email"]
            return JsonResponse({"success": False, "error_message": error_message, "url": reverse("login")})
    else:
        return render(request, "change_password.html")


@login_required(login_url="login")
def delete_account(request, id):
    # POST request
    if request.method == "POST":
        if request.user.id != id:
            return JsonResponse({"success": False, "message": "You do not have permission to perform this action"})
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password == "":
            return JsonResponse({"success": False, "message": "Enter password"})
        if password != confirmation:
            return JsonResponse({"success": False, "message": "Password does not equal confirmation"})
        authenticated = authenticate(
            request, username=request.user.username, password=password)
        if authenticated is not None:
            user = User.objects.get(pk=id)
            user.delete()
            return JsonResponse({"success": True, "url": reverse("logout")})
        else:
            return JsonResponse({"success": False, "message": "Incorrect Password"})


@login_required(login_url="login")
def edit_settings(request):
    # POST request
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        new_books = request.POST.get("new-books", "")
        updates = request.POST.get("follow-updates", "")
        sales = request.POST.get("sales", "")
        wish_sales = request.POST.get("wish-sales", "")

        if new_books == "":
            user.can_send_new = False
        else:
            user.can_send_new = True
        if updates == "":
            user.can_send_updates = False
        else:
            user.can_send_updates = True
        if sales == "":
            user.can_send_sales = False
        else:
            user.can_send_sales = True
        if wish_sales == "":
            user.can_send_wish_sales = False
        else:
            user.can_send_wish_sales = True
        user.save()
        return JsonResponse({"success": True})


@login_required(login_url="login")
def profile_view(request, id):
    # GET request views page, display username, email address on file (if user == user accessing), wishlist + following
    current_user = User.objects.get(pk=id)
    wishlist = Wish.objects.filter(user=id).order_by("-date_added")
    series_followed = Follow.objects.filter(follower=id)

    context = {
        "current_user": current_user,
        "wishlist": wishlist,
        "series_followed": series_followed,
    }
    return render(request, "profile.html", context)


@login_required(login_url="login")
def add_to_wishlist(request, id):
    # POST request
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        book = Book.objects.get(pk=id)

        try_wish = Wish.objects.filter(user=user, book=book)
        if len(try_wish) > 0:
            try_wish[0].delete()
            return JsonResponse({"action": "remove"})
        else:
            add_wish = Wish(user=user, book=book)
            add_wish.save()
            return JsonResponse({"action": "add"})


@login_required(login_url="login")
def follow_series(request, id):
    # POST request
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        series = Series.objects.get(pk=id)

        try_follow = Follow.objects.filter(follower=user, series=series)
        if len(try_follow) > 0:
            try_follow[0].delete()
            return JsonResponse({"action": "remove"})
        else:
            follow = Follow(follower=user, series=series)
            follow.save()
            return JsonResponse({"action": "add"})

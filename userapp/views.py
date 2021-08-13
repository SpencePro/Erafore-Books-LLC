from django.contrib import auth
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.http import HttpResponseRedirect
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
            return HttpResponseRedirect(reverse("index"))
        else:
            context = {
                "message": "Invalid login credentials",
            }
            return render(request, "login.html", context)
    else:
        return render(request, "login.html")


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    # GET request loads page, POST request submits
    error_message = ""

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # check length of username
        if len(username) < 6:
            error_message = "Invalid username"
            return render(request, "register.html", context={"error_message": error_message})

        # validate password
        validate = validate_pword(password, confirmation, username)
        if validate != None:
            return render(request, "register.html", context={"error_message": validate})

        # username must be unique
        try_user = User.objects.filter(username=username)
        if len(try_user) > 0:
            error_message = "Invalid username"
            return render(request, "register.html", context={"error_message": error_message})
        else:
            # send email to user with code, if they enter code successfully, activate account
            passcode = random.randint(100000, 1000000)
            verify_account(email, passcode)
            request.session["passcode"] = passcode
            request.session["username"] = username
            request.session["email"] = email
            request.session["password"] = password
            # use AJAX to create form on same page instead of using new HTML page
            return render(request, "verify_email.html")
    else:
        return render(request, "register.html", context={"error_message": error_message})


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
            return HttpResponseRedirect(reverse("login"))
        else:
            error_message = "Incorrect Passcode"
            del request.session["passcode"]
            del request.session["username"]
            del request.session["email"]
            del request.session["password"]
            return render(request, "register.html", context={"error_message": error_message})


# reset user's password if they forget it
def reset_password(request):
    # POST request
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        
        user = User.objects.filter(username=username, email=email)
        if len(user) < 1:
            return render(request, "login.html", context={"message": "Invalid credentials"})
        else:
            passcode = random.randint(100000, 1000000)
            change_password(email, passcode)
            request.session["passcode"] = passcode
            request.session["username"] = username
            request.session["email"] = email
            return render(request, "change_password.html")


def verify_reset(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        user_submission = int(request.POST["passcode"])
        passcode = int(request.session["passcode"])
        username = request.session["username"]
        email = request.session["email"]
        
        validate = validate_pword(password, confirmation, username)
        if validate != None:
            return render(request, "change_password.html", context={"error_message": validate})

        '''# Check password length
        if len(password) < 8:
            error_message = "Invalid password"
            return render(request, "change_password.html", context={"error_message": error_message})
        # Check that password == confirmation
        if password != confirmation:
            error_message = "Password and confirmation do not match"
            return render(request, "change_password.html", context={"error_message": error_message})
        # password must contain at least 1 special character, 1 number and 1 capital letter
        upper_count = 0
        special_count = 0
        num_count = 0

        for character in password:
            if character.isupper():
                upper_count += 1
            elif not character.isalnum():
                special_count += 1
            elif character.isdigit():
                num_count += 1

        if upper_count == 0 or num_count == 0 or special_count == 0:
            error_message = "Invalid password"
            return render(request, "change_password.html", context={"error_message": error_message})
        # Verify username
        if username == password:
            error_message = "Invalid password"
            return render(request, "change_password.html", context={"error_message": error_message})'''

        # Verify user's passcode
        if user_submission == passcode:
            user = User.objects.get(username=username, email=email)
            new_password = make_password(password)
            user.password = new_password
            user.save()
            del request.session["passcode"]
            del request.session["username"]
            del request.session["email"]
            return HttpResponseRedirect(reverse("login"))
        else:
            error_message = "Incorrect Passcode"
            del request.session["passcode"]
            del request.session["username"]
            del request.session["email"]
            return render(request, "login.html", context={"error_message": error_message})


@login_required(login_url="login")
def delete_account(request, id):
    # POST request
    # use AJAX to display error messages
    if request.method == "POST":
        if request.user.id != id:
            print("You do not have permission to perform this action")
            return HttpResponseRedirect(reverse("profile", kwargs={"id": request.user.id}))
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password == "":
            print("Enter password")
            return HttpResponseRedirect(reverse("profile", kwargs={"id": request.user.id}))
        if password != confirmation:
            print("Password does not equal confirmation")
            return HttpResponseRedirect(reverse("profile", kwargs={"id": request.user.id}))
        authenticated = authenticate(
            request, username=request.user.username, password=password)
        if authenticated is not None:
            user = User.objects.get(pk=id)
            user.delete()
            return HttpResponseRedirect(reverse("logout"))
        else:
            print("Incorrect Password")
            return HttpResponseRedirect(reverse("profile", kwargs={"id": request.user.id}))


@login_required(login_url="login")
def edit_settings(request):
    # POST request
    # use AJAX
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

        return HttpResponseRedirect(reverse("profile", kwargs={"id": user.id}))


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
    # update with AJAX
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        book = Book.objects.get(pk=id)
        page = request.POST["page"]

        try_wish = Wish.objects.filter(user=user, book=book)
        if len(try_wish) > 0:
            try_wish[0].delete()
        else:
            add_wish = Wish(user=user, book=book)
            add_wish.save()
    
    if page == "profile":
        return HttpResponseRedirect(reverse("profile", kwargs={"id": user.id}))
    else:
        return HttpResponseRedirect(reverse("book", kwargs={"id": book.id}))


@login_required(login_url="login")
def follow_series(request, id):
    # POST request
    # update with AJAX
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        series = Series.objects.get(pk=id)
        page = request.POST["page"]

        try_follow = Follow.objects.filter(follower=user, series=series)
        if len(try_follow) > 0:
            try_follow[0].delete()
        else:
            follow = Follow(follower=user, series=series)
            follow.save()
    
    if page == "profile":
        return HttpResponseRedirect(reverse("profile", kwargs={"id": user.id}))
    else:
        book = request.POST["book"]
        return HttpResponseRedirect(reverse("book", kwargs={"id": int(book)}))

from django.shortcuts import render
from django.core.mail import send_mail, send_mass_mail
import random

from userapp.models import User, Follow, Wish
from mainapp.models import Book, Series


# function to continuously check database for book/series updates
def check_series(request):
    
    return


# function to send an email to all users who are following a series when it updates
def send_series_update(request):
    
    return


# function to send an email to all users when a new book comes out
def new_book_notification(request):
    return


# function to send notifications of sales
def send_sales_notification(request):
    return


# function to send email to user to verify their email address/password for account creation
def verify_account(email, passcode):
    send_mail(
        "Register Your Account",
        f"Your passcode is: {passcode}.\nPlease enter this code in the website to complete your registration.",
        "",
        [email],
        fail_silently=True
    )


# function to send email to user to change password
def change_password(email, passcode):
    send_mail(
        "Reset Your Password",
        f"Your passcode is: {passcode}.\nPlease use this code in the website to complete your password reset.",
        "",
        [email],
        fail_silently=True
    )


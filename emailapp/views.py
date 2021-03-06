from django.shortcuts import render
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.utils import html
from django.utils.html import strip_tags
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.core.signals import request_finished
import datetime

from userapp.models import User, Follow, Wish
from mainapp.models import Book, Series


# function to send an email to all users when a new book comes out or when a series the user follows is updated
@receiver(post_save, sender=Book)
def new_book_notification(sender, **kwargs):
    # get the most recently released book
    try:
        book = Book.objects.get(date_released=datetime.date.today())
    except:
        return
    users = User.objects.filter(can_send_new=True)
    if len(users) < 1:
        return
    # get the series that book is in
    series = book.series
    # get all users who are following that series
    series_followers = Follow.objects.filter(series=series)
    if len(series_followers) > 0:
        follow_users = [follower.follower for follower in series_followers]
    
    already_sent = []
    subject = f"New book released: {book.title}"

    # send email to users who are just signed up to receive newsletter
    for user in users:
        if user.username.startswith("newsletter-user-"):
            passcode = user.username[16:]
            html_message = render_to_string("mail_template.html", {"book_title": book.title, "book_synopsis": book.synopsis, "amazon_link": book.amazon_link, "user_account": False, "user_id": int(user.id), "email": user.email, "passcode": passcode})
            plain_message = strip_tags(html_message)
            send_mail(subject, plain_message, "", [user.email], html_message=html_message)
            already_sent.append(user)
            
    # send emails to users who are following the updated series
    if len(series_followers) > 0:
        for user in follow_users:
            if user.can_send_updates == True:
                html_message = render_to_string("mail_template.html", {"book_title": book.title, "book_synopsis": book.synopsis, "amazon_link": book.amazon_link, "user_account": True})
                plain_message = strip_tags(html_message)
                send_mail(subject, plain_message, "", [user.email], html_message=html_message)
                already_sent.append(user)
    # send emails to users who consent to receive all new release notifications, who have not already been emailed
    for user in users:
        if user not in already_sent:
            html_message = render_to_string("mail_template.html", {"book_title": book.title, "book_synopsis": book.synopsis, "amazon_link": book.amazon_link, "user_account": True})
            plain_message = strip_tags(html_message)
            send_mail(subject, plain_message, "", [user.email], html_message=html_message)

    '''email_tuple = tuple(email_arr)
    send_mass_mail(
        email_tuple, fail_silently=False
    )'''


# function to send notifications of sales
@receiver(post_save, sender=Book)
def send_sales_notification(sender, instance, **kwargs):
    # check if instance of model that was saved was set to true; if not, no need to send notifications, end function
    book = Book.objects.get(id=instance.id)
    if book.on_sale == False:
        return
    else:
        # get all users who have that book in their wishlist
        all_users = {}
        wishes = Wish.objects.filter(book=book)
        for wish in wishes:
            all_users[wish.user] = wish.book

        wish_users = [*all_users]
        already_sent = []

        # get all users who allow sales emails
        sales_users = User.objects.filter(can_send_sales=True)
        if len(sales_users) < 1:
            pass

        subject = f"On Sale Now: {book.title}"
        sale_email = True

        # send email to all users who consent to notifications when a book in their wishlist goes on sale
        for user in wish_users:
            if user.can_send_wish_sales == True:
                html_message = render_to_string("mail_template.html", {"book_title": book.title, "book_synopsis": book.synopsis, "amazon_link": book.amazon_link, "user_account": True, "sale": sale_email})
                plain_message = strip_tags(html_message)
                send_mail(subject, plain_message, "", [user.email], html_message=html_message)
                already_sent.append(user)

        # send email to all users who consent to all sales notifications, except for those who have been emailed already
        for user in sales_users:
            if user not in already_sent:
                html_message = render_to_string("mail_template.html", {"book_title": book.title, "book_synopsis": book.synopsis, "amazon_link": book.amazon_link, "user_account": True, "sale": sale_email})
                plain_message = strip_tags(html_message)
                send_mail(subject, plain_message, "", [user.email], html_message=html_message)

        '''email_tuple = tuple(email_arr)
        send_mass_mail(
            email_tuple, fail_silently=True
        )'''


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

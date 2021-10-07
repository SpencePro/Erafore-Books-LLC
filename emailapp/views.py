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
    print("new book")
    try:
        book = Book.objects.get(date_released=datetime.date.today())
    except:
        return
    users = User.objects.filter(can_send_new=True)
    if len(users) < 1:
        return
    print("new book:", book.title)
    # get the series that book is in
    series = book.series
    # get all users who are following that series
    series_followers = Follow.objects.filter(series=series)
    '''if len(series_followers) < 1:
        return'''
    follow_users = [follower.follower for follower in series_followers]

    email_arr = []
    already_sent = []
    subject = f"New book released: {book.title}"
    email_body = f"On sale now from Erafore Books: {book.title}\n\n'{book.synopsis}'\n\nClick here to purchase on Amazon:\n{book.amazon_link}"

    # send email to users who are just signed up to receive newsletter
    for user in users:
        if user.username.startswith("newsletter-user-"):
            passcode = user.username[16:]
            '''
            email_body += f"\n\nUnsubscribe at http://127.0.0.1:8000/user/unsubscribe/{int(user.id)}/{user.email}/{passcode}"
            user_message = (subject, email_body, "", [user.email])
            email_arr.append(user_message)
            already_sent.append(user)
            '''
            html_message = render_to_string("mail_template.html", {"book_title": book.title, "book_synopsis": book.synopsis, "amazon_link": book.amazon_link, "user_account": False, "user_id": int(user.id), "email": user.email, "passcode": passcode})
            plain_message = strip_tags(html_message)
            send_mail(subject, plain_message, "", [user.email], html_message=html_message)
            already_sent.append(user)
            
    # send emails to users who are following the updated series
    for user in follow_users:
        if user.can_send_updates == True:
            email_body += "\n\nYou can edit email permissions in your account anytime at www.eraforebooks.com"
            user_message = (subject, email_body, "", [user.email])
            email_arr.append(user_message)
            already_sent.append(user)
    # send emails to users who consent to receive all new release notifications, who have not already been emailed
    for user in users:
        if user not in already_sent:
            email_body += "\n\nYou can edit email permissions in your account anytime at www.eraforebooks.com"
            user_message = (subject, email_body, "", [user.email])
            email_arr.append(user_message)

    email_tuple = tuple(email_arr)
    send_mass_mail(
        email_tuple, fail_silently=False
    )


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
        email_arr = []
        already_sent = []

        # get all users who allow sales emails
        sales_users = User.objects.filter(can_send_sales=True)
        if len(sales_users) < 1:
            return

        # send email to all users who consent to notifications when a book in their wishlist goes on sale
        for user in wish_users:
            if user.can_send_wish_sales == True:
                book_title = book.title
                book_link = book.amazon_link
                synopsis = book.synopsis

                subject = f"On sale now: {book_title}"
                email_body = f"On sale now from Erafore Books: {book_title}\n\n'{synopsis}'\n\nClick here to purchase on Amazon:\n{book_link}\n\nYou have consented to receive notifications of book sales from Erafore Books, LLC for books in your wishlist. You can edit email permissions in your account anytime at www.eraforebooks.com"

                user_message = (subject, email_body, "", [user.email])
                email_arr.append(user_message)
                already_sent.append(user)

        # send email to all users who consent to all sales notifications, except for those who have been emailed already
        for user in sales_users:
            if user not in already_sent:
                book_title = book.title
                book_link = book.amazon_link
                synopsis = book.synopsis

                subject = f"On sale now: {book_title}"
                email_body = f"On sale now from Erafore Books: {book_title}\n\n'{synopsis}'\n\nClick here to purchase on Amazon:\n{book_link}\n\nYou have consented to receive notifications of book sales from Erafore Books, LLC. You can edit email permissions in your account anytime at www.eraforebooks.com"

                user_message = (subject, email_body, "", [user.email])
                email_arr.append(user_message)

        email_tuple = tuple(email_arr)
        send_mass_mail(
            email_tuple, fail_silently=True
        )


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

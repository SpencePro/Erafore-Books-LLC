from django.shortcuts import render
from django.core.mail import send_mail, send_mass_mail
from django.core.signals import request_finished
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime

from userapp.models import User, Follow, Wish
from mainapp.models import Book, Series


'''# function to send an email to all users who are following a series when it updates
@receiver(post_save, sender=Book)
def send_series_update(sender, **kwargs):
    # get the most recently released book
    try:
        book = Book.objects.get(date_released=datetime.date.today())
    except:
        return
    # get the series that book is in
    series = book.series
    # get all users who are following that series
    series_followers = Follow.objects.filter(series=series)
    if len(series_followers) < 1:
        return
    users = [follower.follower for follower in series_followers]
    # create email message
    email_arr = []
    subject = f"New book released: {book.title}"
    email_body = f"A new book in a series you are following from Erafore Books has been released: {book.title}\n\n'{book.synopsis}'\n\nClick here to get it on Amazon: {book.amazon_link}\n\nYou have consented to receive notifications of new book releases from Erafore Books, LLC for series you follow. You can edit email permissions in your account anytime at **link to website**"
    # get all users who allow emails to be sent to them
    for user in users:
        if user.can_send_updates == True:
            user_message = (subject, email_body, "", [user.email])
            email_arr.append(user_message)
    email_tuple = tuple(email_arr)
    send_mass_mail(
        email_tuple, fail_silently=True
    )'''


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
    if len(series_followers) < 1:
        return
    follow_users = [follower.follower for follower in series_followers]

    email_arr = []
    already_sent = []
    subject = f"New book released: {book.title}"
    email_body = f"A new book from Erafore Books has been released: {book.title}\n\n'{book.synopsis}'\n\nClick here to get it on Amazon: {book.amazon_link}\n\nYou have consented to receive notifications of new book releases from Erafore Books, LLC. You can edit email permissions in your account anytime at **link to website**"

    # send emails to users who are following the updated series
    for user in follow_users:
        if user.can_send_updates == True:
            user_message = (subject, email_body, "", [user.email])
            email_arr.append(user_message)
            already_sent.append(user)
    # send emails to users who consent to receive all new release notifications, who have not already been emailed
    for user in users:
        if user not in already_sent:
            user_message = (subject, email_body, "", [user.email])
            email_arr.append(user_message)

    email_tuple = tuple(email_arr)
    send_mass_mail(
        email_tuple, fail_silently=True
    )


'''# function to send notifications of sales
@receiver(post_save, sender=Book)
def send_sales_notification(sender, **kwargs):
    # get all books on sale
    books = Book.objects.filter(on_sale=True)
    if len(books) < 1:
        return
    elif len(books) == 1:
        book_title = books[0].title
        book_link = books[0].amazon_link
        synopsis = books[0].synopsis
    else: 
        book_title = ", ".join([book.title for book in books])
        book_link = "\n".join([book.amazon_link for book in books])
        synopsis = "\n\n".join([book.synopsis for book in books])
    # get all users who allow sales emails
    users = User.objects.filter(can_send_sales=True)
    if len(users) < 1:
        return
    email_arr = []
    subject = f"On sale now: {book_title}"
    email_body = f"On sale now from Erafore Books: {book_title}\n\n'{synopsis}'\n\nClick here to purchase on Amazon:\n{book_link}\n\nYou have consented to receive notifications of book sales from Erafore Books, LLC. You can edit email permissions in your account anytime at **link to website**"
    for user in users:
        user_message = (subject, email_body, "", [user.email])
        email_arr.append(user_message)
    email_tuple = tuple(email_arr)
    send_mass_mail(
        email_tuple, fail_silently=True
    )'''


# function to send notification of all sales, and for wishlist
# figure out how to ignore this if sales email was already sent for this book
@receiver(post_save, sender=Book)
def send_sales_notification(sender, **kwargs):
    # get all books on sale
    books = Book.objects.filter(on_sale=True)
    if len(books) < 1:
        return
    # get all users who have each book in their wishlist
    all_users = {} 
    for book in books:
        wishes = Wish.objects.filter(book=book)
        if len(wishes) < 1:
            continue
        for wish in wishes:
            if wish.user not in all_users:
                all_users[wish.user] = [wish.book]
            else:
                all_users[wish.user].append(wish.book)
    if len(all_users) < 1:
        return
    list_users = [*all_users]
    email_arr = []
    already_sent = []

    # get all users who allow sales emails
    sales_users = User.objects.filter(can_send_sales=True)
    if len(sales_users) < 1:
        return
    
    # send email to all users who consent to notifications when a book in their wishlist goes on sale
    for user in list_users:
        if user.can_send_wish_sales == True:
            book_count = all_users[user]
            if len(book_count) == 1:
                book_title = book_count[0].title
                book_link = book_count[0].amazon_link
                synopsis = book_count[0].synopsis
            else:
                book_title = ", ".join([book.title for book in book_count])
                book_link = "\n".join([book.amazon_link for book in book_count])
                synopsis = "\n\n".join([book.synopsis for book in book_count])
            
            subject = f"On sale now: {book_title} - {user.username}"
            email_body = f"On sale now from Erafore Books: {book_title}\n\n'{synopsis}'\n\nClick here to purchase on Amazon:\n{book_link}\n\nYou have consented to receive notifications of book sales from Erafore Books, LLC. You can edit email permissions in your account anytime at **link to website**"
            
            user_message = (subject, email_body, "", [user.email])
            email_arr.append(user_message)
            already_sent.append(user)
            print(user.username)
    # send email to all other users who consent to all sales notifications, except for those who have been emailed already
    for user in sales_users:
        if user not in already_sent:
            if len(books) == 1:
                book_title = books[0].title
                book_link = books[0].amazon_link
                synopsis = books[0].synopsis
            else:
                book_title = ", ".join([book.title for book in books])
                book_link = "\n".join([book.amazon_link for book in books])
                synopsis = "\n\n".join([book.synopsis for book in books])
            
            subject = f"On sale now: {book_title} - {user.username}"
            email_body = f"On sale now from Erafore Books: {book_title}\n\n'{synopsis}'\n\nClick here to purchase on Amazon:\n{book_link}\n\nYou have consented to receive notifications of book sales from Erafore Books, LLC. You can edit email permissions in your account anytime at **link to website**"
            
            user_message = (subject, email_body, "", [user.email])
            email_arr.append(user_message)
            print(user.username)
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

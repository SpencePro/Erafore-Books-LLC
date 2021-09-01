from django import http
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.template import RequestContext
from django.core import serializers
import random
import re
import string

from mainapp.models import Series, Book, LoreObject
from userapp.models import Wish, Follow


def index(request):
    # GET request
    books = Book.objects.all()
    sales = [book for book in books if book.on_sale == True]
    new_release = books.order_by("-date_released")[0]

    return render(request, "index.html", context={"books": books, "sales": sales, "new_release": new_release})


def all_books_view(request):
    # GET request shows first 8, POST to show the rest via infinite scroll
    series_list = Series.objects.all()
    selected_series = ""
    selected_world = ""
    worlds = ["Erafore", "Messy Earth", "Terra", "Standalone", ""]
    results_to_show = 8
    
    if request.method == "GET":
        pagenum = 1
        books = Book.objects.all().order_by("-date_released")[0:results_to_show]
    
    else:
        pagenum = int(request.POST["pagenum"])
        books = Book.objects.all().order_by("-date_released")[(pagenum-1)*results_to_show:pagenum*results_to_show]
        books = list(books.values())
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        for book in books:
            date = book["date_released"]
            split_date = str(date).split("-")
            final_timestamp = f"{months[int(split_date[1]) - 1]} {split_date[2]}, {split_date[0]}"
            book["date_released"] = final_timestamp

        return JsonResponse({
            "pagenum": pagenum,
            "books": books,
            "series_list": list(series_list.values()),
            "stop_scrolling": True if len(books) < results_to_show else False # this prevents the server from being called unnecessarily
        })

    context = {
        "num": len(books),
        "selected_series": selected_series,
        "selected_world": selected_world,
        "series_list": series_list,
        "worlds": worlds[:-1],
        "books": books, 
        "pagenum": pagenum
    }
    return render(request, "all_books.html", context)


def filter_books(request):
    series_list = Series.objects.all()
    selected_series = ""
    selected_world = ""
    worlds = ["Erafore", "Messy Earth", "Terra", "Standalone", ""]
    results_to_show = 8

    if request.method == "POST":
        try:
            pagenum = int(request.POST["pagenum"])
        except:
            pagenum = 1
        series_id = request.POST["series"]
        world = request.POST["world"]

        if series_id == "" and world == "":
            return JsonResponse({"error": "Please enter at least one search filter"})
        elif world not in worlds:
            return JsonResponse({"error": "Invalid world"})
        else:
            def filter_without_none(**kwargs):
                return Q(**{k: v for k, v in kwargs.items() if v is not None and v != ""})

            books = Book.objects.filter(
                filter_without_none(series=series_id, world=world)
            ).order_by("-date_released")[(pagenum-1)*results_to_show:pagenum*results_to_show]

            books_data = list(books.values())

            if len(books_data) < 1:
                return JsonResponse({"error": "No books match the filters"})
            
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            for book in books_data:
                date = book["date_released"]
                split_date = str(date).split("-")
                final_timestamp = f"{months[int(split_date[1]) - 1]} {split_date[2]}, {split_date[0]}"
                book["date_released"] = final_timestamp

            if series_id != "":
                selected_series = Series.objects.get(pk=series_id)
                selected_series_name = selected_series.name
                selected_series_description = selected_series.description
            else:
                selected_series_name = None
                selected_series_description = None

            selected_world = world

            return JsonResponse({
                "selected_world": selected_world,
                "selected_series_name": selected_series_name,
                "selected_series_description": selected_series_description,
                "books": books_data,
                "series_list": list(series_list.values()),
                "pagenum": pagenum,
                "stop_scrolling": True if len(books_data) < results_to_show else False
            })


def book_view(request, id):
    # GET request
    book = Book.objects.get(pk=id)
    series = book.series
    follow = ""
    wishlist = ""
    if request.user.is_authenticated:
        follow = Follow.objects.filter(follower=request.user, series=series)
        wishlist = Wish.objects.filter(user=request.user, book=book)

        if len(follow) == 0:
            follow = ""
        if len(wishlist) == 0:
            wishlist = ""

    context = {
        "book": book,
        "following": follow,
        "wishlist": wishlist
    }
    return render(request, "book.html", context)


def contact_view(request):
    # GET request    
    return render(request, "contact.html")


def lore_view(request):
    # GET request displays the default page, POST request displays the page with selected filters
    series_list = Series.objects.all()
    error_message = ""
    world_list = ["Erafore", "Messy Earth", "Terra", "Standalone"]
    type_list = []

    if request.method == "POST":

        series = request.POST["series"]
        world = request.POST["world"]
        type = request.POST["type"]

        if series == "" and world == "" and type == "":
            error_message = "Select at least 1 field to filter"
            lore_objects = LoreObject.objects.all()
        elif series not in series_list or world not in world_list or type not in type_list:
            error_message = "Invalid filter"
            lore_objects = LoreObject.objects.all()
        else:
            # filter only with filters the user selected, ignore if none
            def filter_without_none(**kwargs):
                return Q(**{k: v for k, v in kwargs.items() if v is not None and v != ""})
            
            lore_objects = LoreObject.objects.filter(
                filter_without_none(series=series, world=world, type=type)
            )
                    
    else:
        lore_objects = LoreObject.objects.all()
    
    context = {
        "series_list": series_list,
        "world_list": world_list,
        "type_list": type_list,
        "lore_objects": lore_objects,
        "error_message": error_message
    }
    return render(request, "lorepage.html", context)


def filter_lore(request):
    # POST request
    return


def lore_object_view(request, id):
    # GET request
    lore_object = LoreObject.objects.get(pk=id)
    context = {
        "object": lore_object
    }
    return render(request, "loreobject.html", context)


def search_view(request):
    # GET request; find books, series, lore items
    query = request.GET["q"]
    punct = string.punctuation
    for q in query:
        if q in punct or q == " ":
            query = query.replace(q, "")
    
    if query == "":
        error_message = "Please enter a valid search term"
        context = {
            "query": query,
            "error_message": error_message,
        }
        return render(request, "search_results.html", context)
    
    original_query = query
    books = Book.objects.all()
    #lore_objects = LoreObject.objects.all()
    series_list = Series.objects.all()
    book_matches = []
    #lore_matches = []
    error_message = ""

    r = re.compile(rf"({query})", re.IGNORECASE)

    for book in books:
        book_title = book.title.lower()
        for i in book_title: 
            if i in punct or i == " ":
                book_title = book_title.replace(i, "")
        if query.lower() == book_title:
            return HttpResponseRedirect(reverse("book", kwargs={"id": book.id}))
        else:
            match_title = r.search(book_title)
            if match_title:
                book_matches.append(book)
    
    '''for object in lore_objects:
        object_name = object.name.lower()
        for o in object_name:
            if o in punct or o == " ":
                object_name = object_name.replace(i, "")
        if query.lower() == object_name:
            return HttpResponseRedirect(reverse("lore_object", kwargs={"id": object.id}))
        else:
            match = r.search(object_name)
            if match:
                lore_matches.append(object)'''
    
    for series in series_list:
        series_name = series.name.lower()
        for s in series_name:
            if s in punct or s == " ":
                series_name = series_name.replace(s, "")
        if query.lower() == series_name:
            # find books that are part of the series, append to book_matches
            book_results = Book.objects.filter(series=series)
            for book in book_results:
                book_matches.append(book)
            break
        else:
            match = r.search(series_name)
            if match:
                book_results = Book.objects.filter(series=series)
                for book in book_results:
                    if book not in book_matches:
                        book_matches.append(book)

    if len(book_matches) == 0: # and len(lore_matches) == 0:
        error_message = "There are no results for your search"

    context = {
        "query": original_query,
        "book_num": len(book_matches),
        "books": book_matches,
        # "lore_num": len(lore_matches),
        #"lore_results": lore_matches,
        "error_message": error_message
    }
    return render(request, "search_results.html", context)


def random_view(request):
    # GET request
    books = Book.objects.all()
    rand_num = random.randint(0, len(books)-1)
    id = books[rand_num].id

    return HttpResponseRedirect(reverse("book", kwargs={"id": id}))


def error_404(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 404
    return response


def error_500(request, exception, template_name="500.html"):
    response = render(template_name)
    response.status_code = 500
    return response


# add once debug=False
def back_page(request):
    # GET request
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return

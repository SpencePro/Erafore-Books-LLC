from django import http
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Q
from django.template import RequestContext
import random
import re
import string

from mainapp.models import Series, Book, LoreObject


def index(request):
    # GET request
    return render(request, "index.html")


def all_books_view(request):
    # GET request views all books, POST displays books from series/world that was selected, use AJAX
    # show first 10, use infinite scroll to show more 
    series_list = Series.objects.all()
    selected_series = ""

    if request.method == "POST":
        selected_series = request.POST["series-name"]
        book_list = Book.objects.filter(series=selected_series).order_by("-date_released")

    else:
        book_list = Book.objects.all().order_by("-date_released")
        
    context = {
        "selected_series": selected_series,
        "series_list": series_list,
        "books": book_list
    }
    return render(request, "all_books.html", context)


def book_view(request, id):
    # GET request
    book = Book.objects.get(pk=id)

    context = {
        "book": book
    }
    return render(request, "book.html", context)


def contact_view(request):
    # GET request    
    return render(request, "contact.html")


def lore_view(request):
    # GET request displays the default page, POST request displays the page with selected filters
    series_list = Series.objects.all()
    error_message = ""
    world_list = []
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
            '''
            if series == "" and world == "" and type != "":
                lore_objects = LoreObject.objects.filter(type=type)
            elif series == "" and world != "" and type != "":
                lore_objects = LoreObject.objects.filter(world=world, type=type)
            elif series != "" and world != "" and type != "":
                lore_objects = LoreObject.objects.filter(series=series, world=world, type=type)
            elif series != "" and world != "" and type == "":
                lore_objects = LoreObject.objects.filter(series=series, world=world)
            elif series != "" and world == "" and type == "":
                lore_objects = LoreObject.objects.filter(series=series)
            elif series != "" and world == "" and type != "":
                lore_objects = LoreObject.objects.filter(series=series, type=type)
            elif series == "" and world != "" and type == "":
                lore_objects = LoreObject.objects.filter(world=world)
            '''
                    
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


def lore_object_view(request, id):
    # GET request
    lore_object = LoreObject.objects.get(pk=id)
    context = {
        "object": lore_object
    }
    return render(request, "loreobject.html", context)


def search_view(request):
    # GET request; find books, series, lore items
    query = request.POST["search"]
    books = Book.objects.all()
    lore_objects = LoreObject.objects.all()
    series_list = Series.objects.all()
    book_matches = []
    lore_matches = []
    error_message = ""
    punct = string.punctuation

    for q in query:
        if q in punct or q == " ":
            query = query.replace(q, "")

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
                book_matches.append(book.title)
    
    for object in lore_objects:
        object_name = object.name.lower()
        for o in object_name:
            if o in punct or o == " ":
                object_name = object_name.replace(i, "")
        if query.lower() == object_name:
            return HttpResponseRedirect(reverse("lore_object", kwargs={"id": object.id}))
        else:
            match = r.search(object_name)
            if match:
                lore_matches.append(object.name)
    
    for series in series_list:
        series_name = series.name.lower()
        for s in series_name:
            if s in punct or s == " ":
                series_name = series_name.replace(s, "")
        if query.lower() == series_name:
            # find books that are part of the series, append to book_matches
            book_results = Book.objects.filter(series=series)
            for book in book_results:
                book_matches.append(book.title)
            break
        else:
            match = r.search(series_name)
            if match:
                book_results = Book.object.filter(series=series)
                for book in book_results:
                    if book.title not in book_matches:
                        book_matches.append(book.title)
            
    if len(book_matches) == 0 and len(lore_matches) == 0:
        error_message = "There are no results for your search"

    context = {
        "books": book_matches,
        "lore_results": lore_matches,
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
def back_page(request, path):
    # GET request
    path = str(path)
    return HttpResponseRedirect(reverse())


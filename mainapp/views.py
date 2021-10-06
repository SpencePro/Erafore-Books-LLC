from django import http
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.template import RequestContext
from django.core import serializers
import random, re, string
from mainapp.models import Series, World, Book, LoreObject
from userapp.models import Wish, Follow

def index(request):
    books = Book.objects.all()
    sales = [book for book in books if book.on_sale == True]
    new_release = books.order_by("-date_released")[0]
    quotes = [
    '"What you are does not matter. What you do, does."\n-Goddess Cynthia to Jelly (Royal Ooze Chronicles)', 
    '"Train, and one day honor your dreams by reaching out for them. Grow strong, grow smart, and grow kind. I leave the future in your hands."\n-World-Paladin Tomas Nierz (The Long Road of Adventure)',
    '"Forget video games and the internet, buddy, junk food is what I miss the most about the apocalypse."\n-Jake Trevors (After School Fantasy)',
    '"Zane was curious as to how a blender, a dehumidifier, four computers, eleven gaming consoles and a single Nokia cellphone would possibly be able to make what Rob wanted."\n-Welcome to the Galactic Shoppers Network'
    ]
    for q in quotes:
        quote = quotes[random.randint(0, len(quotes)-1)]
    return render(request, "index.html", context={"books": books, "sales": sales, "new_release": new_release, "quote": quote})


def all_books_view(request, series="", world=""):
    series_list = Series.objects.all()
    worlds = World.objects.all()
    results_to_show = 8
    series_request = False
    series_name = ""
    series_desc = ""
    world_request = False
    world_name = ""
    world_desc = ""

    if request.method == "GET":
        pagenum = 1
        stop_scrolling = False
        if series == "" and world == "":
            books = Book.objects.all().order_by("date_released")[0:results_to_show]
            request.session["objects_viewed"] = results_to_show
        else:
            if series != "":
                books = Book.objects.filter(series=series).order_by("date_released")
                stop_scrolling = True
                series_request = True
                series_name = series_list[int(series)-1].name
                series_desc = books[0].series.description
            else:
                books = Book.objects.filter(world=world).order_by("date_released")
                stop_scrolling = True
                world_request = True
                world_name = worlds[int(world)-1].name
                world_desc = books[0].world.description
    else:
        pagenum = int(request.POST["pagenum"])
        all_books = Book.objects.all().order_by("date_released")
        books = list(all_books[(pagenum - 1) * results_to_show:pagenum * results_to_show].values())
        
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        for book in books:
            date = book["date_released"]
            split_date = str(date).split("-")
            final_timestamp = f"{months[(int(split_date[1]) - 1)]} {split_date[2]}, {split_date[0]}"
            book["date_released"] = final_timestamp
        
        try:
            request.session["objects_viewed"] += len(books)
        except:
            request.session["objects_viewed"] = results_to_show

        if request.session["objects_viewed"] >= len(all_books):
            stop_scrolling = True
            request.session["objects_viewed"] = 0
        else:
            stop_scrolling = False

        return JsonResponse({
            "pagenum": pagenum,
            "books": books,
            "series_list": list(series_list.values()),
            "worlds": list(worlds.values()),
            "stop_scrolling": stop_scrolling # this prevents the server from being called unnecessarily
            })
    
    context = {
        "num": len(books),
        "series_list": series_list,
        "worlds": list(worlds.values()),
        "books": books,
        "pagenum": pagenum,
        "stop_scrolling": stop_scrolling,
        "series_request": series_request,
        "series_name": series_name,
        "selected_series_description": series_desc,
        "world_request": world_request,
        "world_name": world_name,
        "selected_world_description": world_desc
    }
    return render(request, "all_books.html", context)


def filter_books(request):
    series = Series.objects.all()
    series_list = [element["id"] for element in list(series.values())]
    series_list.append("")
    selected_series = ""
    selected_world = ""
    worlds = World.objects.all()
    worlds_list = [element["id"] for element in list(worlds.values())]
    worlds_list.append("")
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
        if world != "":
            if int(world) not in worlds_list:
                return JsonResponse({"error": "Invalid world"})
        if series_id != "":
            if int(series_id) not in series_list:
                return JsonResponse({"error": "Invalid series"})

        def filter_variable_args(**kwargs):
            return Q(**{k: v for k, v in kwargs.items() if v is not None and v != ""})

        book_objects = Book.objects.filter(filter_variable_args(series=series_id, world=world)).order_by(
            "date_released")
        books = list(book_objects[(pagenum - 1) * results_to_show:pagenum * results_to_show].values())
        
        if len(books) < 1:
            return JsonResponse({"error": "No books match the filters"})
        
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        for book in books:
            date = book["date_released"]
            split_date = str(date).split("-")
            final_timestamp = f"{months[(int(split_date[1]) - 1)]} {split_date[2]}, {split_date[0]}"
            book["date_released"] = final_timestamp
        
        if series_id != "":
            selected_series = Series.objects.get(pk=series_id)
            selected_series_name = selected_series.name
            selected_series_description = selected_series.description
        else:
            selected_series_name = None
            selected_series_description = None
        
        if world != "":
            selected_world = World.objects.get(pk=int(world))
            selected_world_name = selected_world.name
            selected_world_description = selected_world.description
        else:
            selected_world_name = None
            selected_world_description = None

        if pagenum == 1:
                request.session["objects_viewed"] = results_to_show
        else:
            request.session["objects_viewed"] += len(books)
        
        if request.session["objects_viewed"] >= len(book_objects):
            stop_scrolling = True
            request.session["objects_viewed"] = 0
        else:
            stop_scrolling = False

        return JsonResponse({
            "selected_world_name": selected_world_name,
            "selected_world_description": selected_world_description,
            "selected_series_name": selected_series_name,
            "selected_series_description": selected_series_description,
            "books": books,
            "series_list": list(series.values()),
            "worlds": list(worlds.values()),
            "pagenum": pagenum,
            "stop_scrolling": stop_scrolling
            })


def book_view(request, id):
    book = Book.objects.get(pk=id)
    series = book.series
    follow = ""
    wishlist = ""
    
    if request.user.is_authenticated:
        follow = Follow.objects.filter(follower=(request.user), series=series)
        wishlist = Wish.objects.filter(user=(request.user), book=book)
        
        if len(follow) == 0:
            follow = ""
        if len(wishlist) == 0:
            wishlist = ""
    
    context = {
        "book":book, 
        "following":follow, 
        "wishlist":wishlist
        }

    return render(request, "book.html", context)


def contact_view(request):
    return render(request, "contact.html")


def lore_view(request):
    series_list = Series.objects.all()
    worlds = World.objects.all()
    type_list = ["Character", "Item", "Place", ""]
    results_to_show = 8
    
    if request.method == "GET":
        pagenum = 1
        lore_data = LoreObject.objects.all()[0:results_to_show]
        request.session["objects_viewed"] = results_to_show
    else:
        pagenum = int(request.POST["pagenum"])
        lore_objects = LoreObject.objects.all()
        lore_data = list(lore_objects[(pagenum - 1) * results_to_show:pagenum * results_to_show].values())
        
        try:
            request.session["objects_viewed"] += len(lore_data)
        except:
            request.session["objects_viewed"] = results_to_show

        if request.session["objects_viewed"] >= len(lore_objects):
            stop_scrolling = True
            request.session["objects_viewed"] = 0
        else:
            stop_scrolling = False

        return JsonResponse({
            "pagenum": pagenum,
            "lore_data": lore_data,
            "series_list": list(series_list.values()),
            "worlds": list(worlds.values()),
            "stop_scrolling": stop_scrolling
            })

    context = {
        "num": len(lore_data),
        "series_list": series_list,
        "worlds": list(worlds.values()),
        "type_list": type_list[:-1],
        "lore_data": lore_data,
        "pagenum": pagenum
        }
    
    return render(request, "lorepage.html", context)


def filter_lore(request):
    series = Series.objects.all()
    series_list = [element["id"] for element in list(series.values())]
    series_list.append("")
    worlds = World.objects.all()
    worlds_list = [element["id"] for element in list(worlds.values())]
    worlds_list.append("")
    type_list = ["Character", "Item", "Place", ""]
    selected_series = ""
    selected_world = ""
    selected_type = ""
    results_to_show = 8
    
    if request.method == "POST":
        try:
            pagenum = int(request.POST["pagenum"])
        except:
            pagenum = 1

        series_id = request.POST["series"]
        world = request.POST["world"]
        type = request.POST["type"]
        
        if series_id == "" and world == "" and type == "":
            return JsonResponse({"error": "Please enter at least one search filter"})

        if world != "":
            if int(world) not in worlds_list:
                return JsonResponse({"error": "Invalid world"})
        if series_id != "":
            if int(series_id) not in series_list:
                return JsonResponse({"error": "Invalid series"})
        if type not in type_list:
            return JsonResponse({"error": "Invalid type"})
        else:
            def filter_variable_args(**kwargs):
                return Q(**{k: v for k, v in kwargs.items() if v is not None and v != ""})

            lore_objects = LoreObject.objects.filter(filter_variable_args(series=series_id, world=world, type=type))
            lore_data = list(lore_objects[(pagenum - 1) * results_to_show:pagenum * results_to_show].values())
            if len(lore_data) < 1:
                return JsonResponse({"error": "No lore matches the filters"})
            
            if series_id != "":
                selected_series = Series.objects.get(pk=series_id)
                selected_series_name = selected_series.name
                selected_series_description = selected_series.description
            else:
                selected_series_name = None
                selected_series_description = None
            
            if series_id != "":
                selected_series = Series.objects.get(pk=series_id)
                selected_series_name = selected_series.name
                selected_series_description = selected_series.description
            else:
                selected_series_name = None
                selected_series_description = None
            
            if world != "":
                selected_world = World.objects.get(pk=int(world))
                selected_world_name = selected_world.name
                selected_world_description = selected_world.description
            else:
                selected_world_name = None
                selected_world_description = None
            
            selected_type = type
            
            if pagenum == 1:
                request.session["objects_viewed"] = results_to_show
            else:
                request.session["objects_viewed"] += len(lore_data)
            
            if request.session["objects_viewed"] >= len(lore_objects):
                stop_scrolling = True
                request.session["objects_viewed"] = 0
            else:
                stop_scrolling = False

    return JsonResponse({
        "worlds": list(worlds.values()),
        "selected_world_name": selected_world_name,
        "selected_world_description": selected_world_description,
        "selected_series_name": selected_series_name,
        "selected_series_description": selected_series_description,
        "selected_type": selected_type,
        "lore_data": lore_data,
        "series_list": list(series.values()),
        "pagenum": pagenum,
        "stop_scrolling": stop_scrolling
        })


"""def lore_object_view(request, id):
    lore_object = LoreObject.objects.get(pk=id)
    context = {"object": lore_object}
    return render(request, "loreobject.html", context)"""


def search_view(request):
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
        #"lore_num": len(lore_matches),
        #"lore_results": lore_matches,
        "error_message": error_message
    }
    return render(request, "search_results.html", context)


def random_view(request):
    books = Book.objects.all()
    rand_num = random.randint(0, len(books) - 1)
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
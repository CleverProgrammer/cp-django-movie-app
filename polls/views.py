from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from airtable import Airtable
import tmdbsimple as tmdb
import os

AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'), 'Movies', api_key=os.environ.get('AIRTABLE_API_KEY'))
tmdb.API_KEY = os.environ.get('TMDB_API_KEY')

# 'https://04rkm6yl.apps.lair.io/'
def index(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query + "', {Name})")
    context = {"search_result": search_result}
    return render(request, "polls/movies.html", context)

def movie_form(request):
    return render(request, "polls/new_movie.html");

def create_movie(request):
    title = request.GET.get('title', '')
    image_url = request.GET.get('image_url', '')
    description = request.GET.get('description', '')
    rating = int(request.GET.get('rating', ''))
    print(image_url)
    new_movie = AT.insert({'Name': title, 'Photos': [{
        "url": image_url,
        "filename": "demo.jpg"
    }],'Description': description, 'PersonalRating': rating})

    context = {"response": "New movie added"}
    return redirect("/my_movies")

def get_my_movies(request):
    movies = AT.get_all()
    context = {"my_movies": movies}
    return render(request, "polls/my_movies.html", context)

def delete_my_movie(request, movie_id):
    AT.delete(movie_id)
    return redirect("/my_movies")

# https://04rkm6yl.apps.lair.io/search/?query=The+Ben
def search_form(request):
    # api.themoviedb.org/3/movie/{id}?api_key={api_key}
    # https://image.tmdb.org/t/p/w500/{image path}
    tmdb_search = tmdb.Search()
    movie_thingy = tmdb_search.movie(query=str(request.GET.get('query', '')) or ' ')
    movie_poster_urls = []
    movie_titles = []
    movies = []

    for movie in movie_thingy['results']:
        movies.append(movie)
        movie_poster_urls.append('https://image.tmdb.org/t/p/w500' + str(movie.get('poster_path', '/')))
        movie_titles.append(movie.get('original_title', ''))
    # https://image.tmdb.org/t/p/w500/xeXW85HF0MWWGQTgewd5thGMf1g.jpg

    # images = movie_thingy.images()
    print(movie_poster_urls)

    # ex: https://04rkm6yl.apps.lair.io/search/?query=5
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query + "', {Name})")

    movies_stuff = zip(movie_titles, movie_poster_urls)
    context = {"search_result": search_result,
               "movies_stuff": movies_stuff,
               "movies": movies}

    return render(request, "polls/movies.html", context)

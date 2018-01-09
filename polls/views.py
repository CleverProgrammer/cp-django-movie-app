from django.shortcuts import render
from django.http import HttpResponse
from airtable import Airtable
import tmdbsimple as tmdb
import os


AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'), 'Movies', api_key=os.environ.get('AIRTABLE_API_KEY'))
tmdb.API_KEY = os.environ.get('TMDB_API_KEY')


def index(request):
    context = {}
    return render(request, "polls/movies.html", context)

def search_form(request):


    # api.themoviedb.org/3/movie/{id}?api_key={api_key}
    # https://image.tmdb.org/t/p/w500/{image path}
    # for movie in movie_thingy['results'] get me movie['poster_path']
    tmdb_search = tmdb.Search()
    movie_thingy = tmdb_search.movie(query=str(request.GET.get('query', '')))
    movie_poster_urls = []
    movie_titles = []

    for movie in movie_thingy['results']:
        movie_poster_urls.append('https://image.tmdb.org/t/p/w500' + str(movie['poster_path']))
        movie_titles.append(movie['original_title'])
    # https://image.tmdb.org/t/p/w500/xeXW85HF0MWWGQTgewd5thGMf1g.jpg

    # images = movie_thingy.images()
    print(movie_poster_urls)

    # ex: https://04rkm6yl.apps.lair.io/search/?query=5
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query + "', {Name})")

    movies_stuff = zip(movie_titles, movie_poster_urls)
    context = {"search_result": search_result,
               "movies_stuff": movies_stuff}

    return render(request, "polls/movies.html", context)

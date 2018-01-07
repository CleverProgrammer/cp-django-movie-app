from django.shortcuts import render
from django.http import HttpResponse
from airtable import Airtable
import os


AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'), 'Movies', api_key=os.environ.get('AIRTABLE_API_KEY'))
# AT = Airtable(AIRTABLE_MOVIESTABLE_BASE_ID, 'Movies', api_key=AIRTABLE_API_KEY)


def index(request):


    # result = at.get('Movies')
    # print(result)

    context = {}
    return render(request, "polls/movies.html", context)

    #template = loader.get_template("polls/movies.html")
    #return HttpResponse(template.render())

    #return HttpResponse("Hello, world. You're at the polls index.")

def search_form(request):

    # result = at.get('Movies')

    # ex: https://04rkm6yl.apps.lair.io/search/?query=5
    user_query = str(request.GET.get('query', ''))

    # contains search example... (sort of lol)
    #
    # = 1 means exact match (one)
    #search_result = AT.get_all(formula="FIND('" + user_query + "', {Name})=1")
    #
    # This is more like contains
    #
    search_result = AT.get_all(formula="FIND('" + user_query + "', {Name})")
    context = {"search_result": search_result}

    return render(request, "polls/movies.html", context)

from django.urls import path
from django.conf.urls import url


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_movie', views.movie_form, name="movie_form"),
    path('my_movies', views.get_my_movies, name="my_movies"),
    url('create_movie', views.create_movie, name='create_movie'),
    path('my_movies/<movie_id>/', views.delete_my_movie),
    url(r'^search/$', views.search_form)
]
#[a-zA-Z0-9]+

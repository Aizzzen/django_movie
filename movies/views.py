from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Movie


# class MoviesView(View):
#     def get(self, request):
#         movies = Movie.objects.all()
#         return render(request, "movies/movie_list.html", {"movie_list": movies})


# class MoviesDetailView(View):
#     def get(self, request, slug):
#         movie = Movie.objects.get(url=slug)
#         return render(request, "movies/movie_detail.html", {"movie": movie})


class MoviesView(ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    # Django самостоятельно отрисует шаблон, взяв имя модели и добавив _list (т.к. ListView)
    # получится movie_list
    # template_name = "movies/movie_list.html"


class MoviesDetailView(DetailView):
    model = Movie
    slug_field = "url"

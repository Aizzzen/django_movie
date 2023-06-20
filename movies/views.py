from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import AddReviewForm
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


class AddReview(View):
    def post(self, request, pk):
        # при post запросе объект request имеет массив передаваемых параметров POST
        # forms - Формы - используются для валидации
        # ссылочные поля в модели Джанго хранятся по id, поэтому такие данные можно добавлять 2 способами:
        # 1 - movie_id = pk ||||| movie = Movie.objects.get(id=pk) + form.movie = movie
        form = AddReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False) # останавливаем сохранение объекта для его дополнения
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            # form.movie_id = pk
            form.movie = movie
            form.save() # ОБЯЗАТЕЛЬНО СОХРАНЯТЬ В КОНЦЕ
        return redirect(movie.get_absolute_url())

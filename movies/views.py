from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import AddReviewForm
from .models import Movie, Category, Actor, Genre


# class MoviesView(View):
#     def get(self, request):
#         movies = Movie.objects.all()
#         return render(request, "movies/movie_list.html", {"movie_list": movies})


# class MoviesDetailView(View):
#     def get(self, request, slug):
#         movie = Movie.objects.get(url=slug)
#         return render(request, "movies/movie_detail.html", {"movie": movie})


# для передачи данных в шаблон без использования get_context_data
class GenreYear:
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year") # .values/values_list("year") - указываем только то поле, которое хочу забрать


class MoviesView(GenreYear, ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    # Django самостоятельно отрисует шаблон, взяв имя модели и добавив _list (т.к. ListView)
    # получится movie_list
    # template_name = "movies/movie_list.html"

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! - вместо дублирования кода сделаем movie_tag и передадим в header как categories
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context


class MoviesDetailView(GenreYear, DetailView):
    model = Movie
    slug_field = "url"

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! - вместо дублирования кода сделаем movie_tag и передадим в header как categories
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context


class AddReview(GenreYear, View):
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


class ActorView(GenreYear, DetailView):
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name' # поле по которому будем искать актера


class FormMoviesView(GenreYear, ListView):
    def get_queryset(self):
        queryset = Movie.objects.filter(
            # данный фильтр работает только если выбрать оба условия, т.к. , здесь означает И
            # year__in=self.request.GET.getlist('year'), genre__in=self.request.GET.getlist('genre')

            # чтобы использовать ИЛИ нужно применить метод Q + |
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genre__in=self.request.GET.getlist('genre'))
        )
        return queryset

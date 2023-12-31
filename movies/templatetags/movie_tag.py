from django import template

from movies.models import Category, Movie

register = template.Library()
# создаем экземпляр Library для регистрации тегов


# оборачиваем в деоратор который зарег-т функцию как тег
@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('movies/tags/last_movie.html')
def get_last_movies(count=3):
    movies = Movie.objects.order_by("id")[:count]
    return {'last_movies': movies}

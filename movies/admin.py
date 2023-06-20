from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Actor, Genre, Movie, MovieShots, RatingStar, Rating, Reviews


# конфиг-я полей отображаемых в админке
@admin.register(Category)
# классы для админок можно регистрировать с помощью декоратов, можно напрямую
# admin.site.register(Category, CategoryAdmin)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name", ) # имя поля которое будет ссылкой


class ReviewInline(admin.TabularInline):
    # StackedInline
    # TabularInline - выстроится в виде таблицы
    model = Reviews
    extra = 1 # кол-во доп полей (пустых)
    readonly_fields = ("name", "email")


# прикрепим кадры из фильма к фильму в админке
class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(
            f'<img src={obj.image.url} width="100" height="110">')  # mark_safe - выведет html не как строку а как тег

    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "draft", )
    list_filter = ("category", "year", )
    search_fields = ("title", "category__name", )
    inlines = [MovieShotsInline, ReviewInline] # FK, M2M - для вывод всех отзывов к фильму
    save_on_top = True # панель сохранения наверху
    save_as = True # удобно при создании новых записей
    list_editable = ("draft", ) # поля которые можно изменять сразу у нескольких объектов одновременно
    # fields = (("actors", "directors", "genre", ), ) # группируем поля в строку, + убрать лишние поля
    # + 1 поля для группировки полей
    readonly_fields = ("get_image", )
    fieldsets = (
        # группы полей можно давать имена и скрывать их
        (None, {
            "fields": (("title", "tagLine"), ) # элементы в кортеже в кортеже будут в одну стоку
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"))
        }),
        (None, {
            "fields": (("year", "premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse", ), # скрыть поле
            "fields": (("actors", "directors", "genre", "category"), )
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world",),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(
            f'<img src={obj.poster.url} width="100" height="110">')  # mark_safe - выведет html не как строку а как тег

    get_image.short_description = "Постер"


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email") # закрыть для редактирования


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "url",)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">') # mark_safe - выведет html не как строку а как тег

    get_image.short_description = "Изображение"


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">') # mark_safe - выведет html не как строку а как тег

    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("star", "ip",)


admin.site.register(RatingStar)
admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"

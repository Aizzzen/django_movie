from datetime import date

from django.db import models


class Category(models.Model):
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание") # TextFiled === без ограничения по длине/кол-ву символов
    url = models.SlugField(max_length=160, unique=True) # SlugFiled - состоит из буквы, цифр, знаков, исполбзуется при составлении url

    def __str__(self): # для получения строкового представления модели
        return self.name

    class Meta: # класс для получения метаданных модели
        verbose_name = "Категория" # имя модели в единственном числе
        verbose_name_plural = "Категории" # имя модели во множ числе


class Actor(models.Model):
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="actors/") # ImageField - проверяет является ли изображением

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"


class Genre(models.Model):
    name = models.CharField("Категория", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    title = models.CharField("Название", max_length=100)
    tagLine = models.CharField("Слоган", max_length=100, default="")
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/*")
    year = models.PositiveIntegerField("Дата выхода", default=2023)
    country = models.CharField("Страна", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="режиссер", related_name="film_director") # verbose_name -  для явной передачи имени поля
    actors = models.ManyToManyField(Actor, verbose_name="актеры", related_name="film_actor") # related_name - имя используемое для отношения от связываемого объекта
    genre = models.ManyToManyField(Genre, verbose_name="жанры")
    premiere = models.DateTimeField("Премьера", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="указывать сумму в долларах")
    fees_in_usa = models.PositiveIntegerField("Сборы в США", default=0, help_text="указывать сумму в долларах")
    fees_in_world = models.PositiveIntegerField("Сборы в мире", default=0, help_text="указывать сумму в долларах")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True) # on_delete=models.SET_NULL - при удалении объекта связанного с полем, оно станет null, + null = True
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieShots(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class RatingStar(models.Model):
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"


class Rating(models.Model):
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, verbose_name="звезда", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CharField)

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True) # blank=True - поле м.б. пустым
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
from django.db import models
from user.models import User


class Genre(models.Model):
    name = models.TextField(
        max_length=256,
        verbose_name='Название',
        help_text='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Slug',
        help_text='Slug жанра'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(
        max_length=256,
        verbose_name='Название',
        help_text='Название произведения'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        help_text='Год выпуска произведения'
    )
    description = models.TextField(
        blank=True, null=True,
        verbose_name='Описание',
        help_text='Описание произведения'
    )
    rating = models.IntegerField(
        blank=True, null=True,
        verbose_name='Рейтинг',
        help_text='Рейтинг произведения'
    )
    # rating = models.ForeignKey()  Пока не знаю, на что ссылаться.
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр',
        help_text='Жанр, к которому принадлежит произведение'
    )
    category = models.ForeignKey(
        'Category',
        # blank=False,
        null=True,
        on_delete=models.SET_NULL,
        # default="",
        # on_delete=models.SET_DEFAULT,
        # on_delete=models.DO_NOTHING,
        verbose_name='Категория',
        help_text='Категория, к которой принадлежит произведение'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.TextField(
        max_length=256,
        verbose_name='Название',
        help_text='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Slug',
        help_text='Slug категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
        

class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    score = models.IntegerField(verbose_name='Оценка')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    text = models.TextField(verbose_name='Текст')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]

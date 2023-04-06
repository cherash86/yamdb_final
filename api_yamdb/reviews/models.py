import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(
        'Имя категории',
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        'URL категории',
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Имя жанра',
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        'URL жанра',
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=200
    )
    year = models.IntegerField(
        'Год выхода произведения',
        validators=[
            MinValueValidator(-3000),
            MaxValueValidator(datetime.datetime.now().year)
        ]
    )
    description = models.TextField(
        'Описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="categories",
        verbose_name="Категория",
    )
    genre = models.ManyToManyField(
        Genre,
        blank=False,
        verbose_name="Жанр",
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['pub_date']


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Произведение",
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Автор",
    )
    text = models.TextField(
        'Текст отзыва'
    )
    score = models.IntegerField(
        'Оценка',
        validators=[MaxValueValidator(10), MinValueValidator(1)])
    pub_date = models.DateTimeField(
        'Дата отзыва',
        auto_now_add=True
    )

    class Meta:
        ordering = ['pub_date']
        constraints = [models.UniqueConstraint(fields=['title', 'author'],
                                               name="unique_review_author")]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Комментарий",
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Автор",
    )
    text = models.TextField(
        'Текст комментария'
    )
    pub_date = models.DateTimeField(
        'Дата комментария',
        auto_now_add=True
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ['pub_date']

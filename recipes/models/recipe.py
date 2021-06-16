from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.db import models

from .ingredient import Ingredient
from .tag import Tag

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.DO_NOTHING,
        related_name='recipes',
        verbose_name='Автор',
        help_text='Введите автора рецепта',
        null=True
    )
    title = models.CharField(
        verbose_name='Название',
        help_text='Введите название рецепта',
        max_length=50, blank=False, null=False
    )
    description = RichTextUploadingField(
        verbose_name='Описание рецепта',
        help_text='Введите описание рецепта',
        blank=False, null=False
    )
    ingredients = models.ManyToManyField(
        Ingredient, related_name='in_recipes',
        verbose_name='Ингредиенты',
        help_text='Выберите ингредиенты',
        through='QuantityIngredient',
        blank=False
    )
    tag = models.ManyToManyField(
        Tag, related_name='in_recipes',
        verbose_name='Тег',
        help_text='Выберите теги',
    )
    slug = AutoSlugField(
        populate_from='title',
        verbose_name='Слаг рецепта',
        help_text='Краткий url рецепта',
        unique=True
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        help_text='Введите время приготовления в минутах',
        null=False, blank=False
    )
    image = models.ImageField(
        verbose_name='Картинка рецепта',
        help_text='Вы можете прикрепить к своему рецепту картинку',
        upload_to='recipes/',
        default='testCardImg.png',
        blank=True,
        null=True
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return f'Рецепт {self.title}'

from django.contrib.auth import get_user_model
from django.db import models

from .recipe import Recipe

User = get_user_model()


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='shoplists',
        verbose_name='Пользователь',
        help_text='Выберите пользователя'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='shoplists',
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )

    def __str__(self):
        return f'Шоп. Лист для {self.user}'

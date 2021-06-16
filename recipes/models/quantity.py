from django.db import models

from .ingredient import Ingredient
from .recipe import Recipe


class QuantityIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='quantity_ingredients',
        verbose_name='Рецепт',
        help_text='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='quantity_ingredients',
        verbose_name='Ингредиент',
        help_text='Выберите ингредиент',
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество ингредиента',
        help_text='Введите количество ингредиента',
        null=False, blank=False
    )

    def __str__(self):
        title = self.ingredient.title
        dimension = self.ingredient.dimension
        return f'{title} - {self.quantity}{dimension}'

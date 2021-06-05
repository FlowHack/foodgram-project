from django.db import models

from .ingredient import Ingredient


class QuantityIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
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

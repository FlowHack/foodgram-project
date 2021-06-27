from django.db import models


class Ingredient(models.Model):
    title = models.CharField(
        verbose_name='Ингредиент',
        help_text='Введите ингредиент',
        max_length=100,
        null=False, blank=False
    )
    dimension = models.CharField(
        verbose_name='Измерение',
        help_text='В чём измеряется',
        max_length=40,
        null=False, blank=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['dimension', 'title'], name='unique dimension'
            )
        ]

    def __str__(self):
        return f'{self.title} {self.dimension}'

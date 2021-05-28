from django.db import models


class Tag(models.Model):
    title = models.CharField(
        verbose_name='Тег',
        help_text='Введите название тега',
        max_length=20, blank=False, null=False
    )
    tag = models.CharField(
        verbose_name='Значение',
        help_text='Введите значение тега',
        max_length=20, blank=False, null=False
    )

    def __str__(self):
        return self.title

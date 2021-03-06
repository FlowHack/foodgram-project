from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        blank=False, unique=True
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        verbose_name='На кого подписан',
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique author'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='users_cannot_follow_themselves'
            )
        ]
        ordering = ['-id']

    def __str__(self):
        return f'{self.user} подписан на {self.author}'

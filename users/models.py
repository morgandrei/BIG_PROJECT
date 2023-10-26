from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Пользователи сервиса рассылок"""
    username = None
    email = models.EmailField(max_length=100, verbose_name='почта', unique=True)
    avatar = models.ImageField(upload_to='users', **NULLABLE)
    phone = models.CharField(max_length=20, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=20, verbose_name='страна', **NULLABLE)
    token = models.CharField(max_length=100, **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}' or ''

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

        permissions = [
            (
                'set_activity',
                'Can change activity'
            )
        ]

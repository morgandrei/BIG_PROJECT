from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Клиент"""
    email = models.EmailField(verbose_name='почта', unique=True)
    name = models.CharField(max_length=100, verbose_name='имя')
    surname = models.CharField(max_length=100, verbose_name='фамилия')
    patronymic = models.CharField(max_length=100, verbose_name='отчество', **NULLABLE)
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.name} {self.surname} - {self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

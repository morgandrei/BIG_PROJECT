from django.contrib.auth import get_user_model
from django.db import models

from users.models import User, NULLABLE

class Client(models.Model):
    """Клиент"""
    email = models.EmailField(verbose_name='контактный email')
    fullname = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, verbose_name='клиент', **NULLABLE)

    def __str__(self):
        return f'{self.fullname} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Newsletter(models.Model):
    """Рассылка"""
    FREQUENCY_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    ]

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    mailing_time = models.DateTimeField(verbose_name='время рассылки', **NULLABLE)
    periodicity = models.DateTimeField(choices=FREQUENCY_CHOICES, verbose_name='периодичность')
    mailing_status = models.CharField(max_length=100, choices=STATUS_CHOICES, verbose_name='статус рассылки')
    recipient = models.ManyToManyField(User, related_name='newsletters', verbose_name='получатели')

    def __str__(self):
        return self.mailing_status

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class MailingMessage(models.Model):
    """Сообщение для рассылки"""
    subject = models.CharField(max_length=100, verbose_name='тема письма')
    content = models.TextField(verbose_name='тело письма')
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, null=True, related_name='messages',
                                   verbose_name='рассылка')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'


class MailingLog(models.Model):
    """Логи рассылки"""
    date = models.DateField(auto_now_add=True, verbose_name='дата попытки')
    time = models.TimeField(auto_now_add=True, verbose_name='время попытки')
    attempt_status = models.BooleanField(default=False, verbose_name='статус попытки')
    server_response = models.TextField(verbose_name='ответ сервера')
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, related_name='logs', verbose_name='рассылка')
    message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE, default=0, related_name='logs',
                                verbose_name='письмо')

    def __str__(self):
        return self.attempt_status

    class Meta:
        verbose_name = 'лог рассылки'
        verbose_name_plural = 'логи рассылок'

class Clients(models.Model):
    pass

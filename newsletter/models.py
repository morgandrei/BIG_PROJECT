from django.contrib.auth import get_user_model
from django.db import models

from users.models import NULLABLE


class Client(models.Model):
    """Клиент"""
    email = models.EmailField(verbose_name='контактный email')
    fullname = models.CharField(max_length=150, verbose_name='клиент')
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
    name = models.CharField(max_length=200, verbose_name='название рассылки', **NULLABLE)
    start_date = models.DateField(default=False, verbose_name='дата рассылки')
    time = models.TimeField(default='00:00', verbose_name='время рассылки')
    frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, default=FREQUENCY_CHOICES[0],
                                 verbose_name='периодичность')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=STATUS_CHOICES[0],
                              verbose_name='статус рассылки')
    clients = models.ManyToManyField(Client, verbose_name='получатели')
    is_active = models.BooleanField(default=True, verbose_name='активность рассылки')
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, verbose_name='пользователь', **NULLABLE)
    message = models.ForeignKey('Message', on_delete=models.CASCADE, verbose_name='сообщение')

    def __str__(self):
        return f'{self.name}({self.pk} {self.user}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            (
                'change_activity',
                'Change activity'
            )
        ]


class Message(models.Model):
    """Сообщение для рассылки"""
    subject = models.CharField(max_length=100, verbose_name='тема письма', **NULLABLE)
    content = models.TextField(verbose_name='тело письма', **NULLABLE)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return self.subject or ''

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'


class Log(models.Model):
    """Логи рассылки"""
    STATUS_LOG = [
        ('success', 'Успешно'),
        ('failure', 'Ошибка'),
    ]

    datetime = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    status = models.CharField(max_length=10, choices=Newsletter.STATUS_CHOICES, verbose_name='статус попытки')
    server_response = models.TextField(verbose_name='ответ сервера', **NULLABLE)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, verbose_name='рассылка')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, default=0, verbose_name='письмо')

    def __str__(self):
        return f'рассылка {self.newsletter}, статус: {self.status}'

    class Meta:
        verbose_name = 'лог рассылки'
        verbose_name_plural = 'логи рассылок'

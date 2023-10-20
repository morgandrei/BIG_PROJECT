from django.db import models

from users.models import NULLABLE, User


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(max_length=100, verbose_name='slug', **NULLABLE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор')
    content = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(verbose_name='превью', **NULLABLE)
    created_at = models.DateField(auto_now_add=True, verbose_name='дата публикации')
    is_published = models.BooleanField(default=True, verbose_name='признак публикации')
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return f'{self.title} (создано {self.created_at})'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'

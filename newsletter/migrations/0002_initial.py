# Generated by Django 4.2.6 on 2023-11-03 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newsletter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddField(
            model_name='log',
            name='message',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='newsletter.message', verbose_name='письмо'),
        ),
        migrations.AddField(
            model_name='log',
            name='newsletter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsletter.newsletter', verbose_name='рассылка'),
        ),
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='клиент'),
        ),
    ]

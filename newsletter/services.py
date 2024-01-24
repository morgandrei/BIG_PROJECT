import calendar
import datetime

from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.core.mail import send_mail

from blog.models import Blog
from newsletter.models import Log, Newsletter, Client


def get_random_blog_article():
    """Кеширование объектов блога для главной страницы"""
    if settings.CACHE_ENABLED:
        key = 'blog_article'
        blog_article = cache.get(key)
        if blog_article is None:
            blog_article = Blog.objects.order_by('?')[:3]
            cache.set(key, blog_article)
    else:
        blog_article = Blog.objects.order_by('?')[:3]
    return blog_article

def get_cache_count_newsletter():
    if settings.CACHE_ENABLED:
        key = 'newsletter'
        newsletter = cache.get(key)
        if newsletter is None:
            newsletter = Newsletter.objects.all().count()
            cache.set(key, newsletter)
    else:
        newsletter = Newsletter.objects.all().count()
    return newsletter


def get_cache_count_client():
    if settings.CACHE_ENABLED:
        key = 'client'
        client = cache.get(key)
        if client is None:
            client = Client.objects.all().count()
            cache.set(key, client)
    else:
        client = Client.objects.all().count()
    return client


def add_users_group_permissions(group):
    """Добавление разрешений в группу users"""
    permissions = Permission.objects.filter(content_type__model__in=['newsletter', 'message', 'client'])
    for perm in permissions:
        group.permissions.add(perm)


def my_job():
    """Запуск активных рассылок"""
    today = datetime.datetime.now()
    time_now = today.strftime('%H:%M')
    date_today = today.date()
    newsletter_today = Newsletter.objects.filter(start_date=date_today, is_active=True, status=Newsletter.Status.CREATED)
    print(newsletter_today)
    for newsletter in newsletter_today:
        newsletter_time = newsletter.time.strftime('%H:%M')
        print(newsletter)
        print(newsletter_time)

        if newsletter_time <= time_now:
            newsletter.status = Newsletter.Status.RUNNING
            newsletter.save()

            clients = newsletter.clients.all()
            recipient_list = [client.email for client in clients]
            try:
                response = send_mail(newsletter.message.subject, newsletter.message.content, settings.EMAIL_HOST_USER,
                                     recipient_list)
                if response:
                    log = Log(newsletter=newsletter, status=Log.STATUS_LOG[0], server_response=response)
                else:
                    log = Log(newsletter=newsletter, status=Log.STATUS_LOG[1], server_response=response)
                log.save()
            except Exception as response:
                log = Log(newsletter=newsletter, status=Log.STATUS_LOG[1], server_response=response)
                log.save()

            if newsletter.frequency == Newsletter.Frequency.DAILY:
                newsletter.start_date = date_today + datetime.timedelta(days=1)
            elif newsletter.frequency == Newsletter.Frequency.WEEKLY:
                newsletter.start_date = date_today + datetime.timedelta(days=7)
            elif newsletter.frequency == Newsletter.Frequency.MONTHLY:
                days_in_month = calendar.monthrange(today.year, today.month)[1]
                newsletter.start_date = date_today + datetime.timedelta(days=days_in_month)

            newsletter.status = newsletter.Status.CREATED
            newsletter.save()

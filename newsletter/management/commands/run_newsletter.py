from django.core.management import BaseCommand

from newsletter.services import my_job


class Command(BaseCommand):
    help = "Run Mailings"

    def handle(self, *args, **options):
        my_job()

from django.core.management.base import BaseCommand

from api import scrapper


class Command(BaseCommand):
    help = 'Scrapes the Filmoteca website'

    def handle(self, *args, **options):
        scrapper.scrape()

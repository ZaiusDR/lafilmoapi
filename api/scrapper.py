import requests

from lxml import html
from requests.compat import urljoin

from api import models


class WeekScrapper:

    FILMO_URL = 'https://www.filmoteca.cat/web/ca/view-agenda-setmanal'

    def __init__(self, week):
        self.week = week
        self.week_tree = self.get_week_agenda_tree()

    def scrape(self):
        for link in self.scrape_detail_links():
            if '/film' not in link:
                continue
            detail_scrapper = DetailScrapper(link.split('/')[-1])
            film_details = detail_scrapper.scrape_film_details()
            models.Film.objects.update_or_create(**film_details)

    def scrape_detail_links(self):
        return self.week_tree.xpath('//div[@class="titl click_text"]/a/@href')

    def get_week_agenda_tree(self):
        response = requests.get(self.FILMO_URL, params={'w': self.week})
        return html.fromstring(response.content)


class DetailScrapper:
    DETAIL_URL = 'https://www.filmoteca.cat/web/ca/film/'

    def __init__(self, film):
        self.film = film
        self.detail_tree = self.get_detail_agenda_tree()

    def scrape_film_details(self):
        details = {
            'title': self._get_title(),
            'director': self._get_field_value('Direcció'),
            'year': self._get_field_value('Any'),
            'duration': self._get_field_value('Durada')
        }

        return details

    def _get_field_value(self, field):
        return self.detail_tree.xpath(
            f'//span[text()="{field}"]/following-sibling::span/text()'
        )[0]

    def _get_title(self):
        return self.detail_tree.xpath(
            '//div[@class="main-title"]/h1/text()'
        )[0].strip()

    def get_detail_agenda_tree(self):
        response = requests.get(requests.compat.urljoin(self.DETAIL_URL, self.film))
        return html.fromstring(response.content)


def scrape():
    week_scrapper = WeekScrapper('2020-02-24')
    week_scrapper.scrape()

import re

import responses

from django.test import TestCase
from django.forms.models import model_to_dict
from rest_framework.test import APIClient
from requests.compat import urljoin

from api import models
from api import scrapper
from api.test_files import week
from api.test_files import detail


class FilmViewTests(TestCase):

    def test_should_return_list_of_films(self):
        client = APIClient()
        film, created = models.Film.objects.update_or_create(
            title="test_title",
            director="test_director",
            year="fake_duration",
            duration="fake_duration"
        )

        response = client.get('/api/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [model_to_dict(film)])


class WeekScrapperTests(TestCase):

    def setUp(self):
        responses.add(responses.GET, scrapper.WeekScrapper.FILMO_URL,
                      body=week.WEEK_HTML, status=200)
        responses.add(responses.GET,
                      re.compile(f'{scrapper.DetailScrapper.DETAIL_URL}.*'),
                      body=detail.FILM_DETAIL_HTML, status=200)

    @responses.activate
    def test_should_scrape_film_detail_links(self):
        week_scrapper = scrapper.WeekScrapper('2020-02-24')

        links = week_scrapper.scrape_detail_links()

        self.assertIs(len(responses.calls), 1)
        self.assertIn('/web/ca/film/werk-ohne-autor', links)

    @responses.activate
    def test_should_save_scrapped_film(self):
        week_scrapper = scrapper.WeekScrapper('2020-02-24')

        week_scrapper.scrape()

        film = models.Film.objects.get(title='Werk ohne Autor')

        assert film.title == 'Werk ohne Autor'
        assert film.director == 'Florian Henckel von Donnersmarck'
        assert film.year == '2018'
        assert film.duration == "188'"


class DetailScrapperTests(TestCase):

    def setUp(self):
        self.test_film = 'werk-ohne-autor'
        responses.add(responses.GET,
                      urljoin(scrapper.DetailScrapper.DETAIL_URL, self.test_film),
                      body=detail.FILM_DETAIL_HTML, status=200)

    @responses.activate
    def test_should_scrape_film_details(self):
        detail_scrapper = scrapper.DetailScrapper(self.test_film)

        film_details = detail_scrapper.scrape_film_details()

        assert len(responses.calls) == 1
        assert film_details['title'] == 'Werk ohne Autor'
        assert film_details['director'] == 'Florian Henckel von Donnersmarck'
        assert film_details['year'] == '2018'
        assert film_details['duration'] == "188'"


class ScrapperIntegrationTests(TestCase):

    def setUp(self):
        self.test_film = 'werk-ohne-autor'
        responses.add(responses.GET, scrapper.WeekScrapper.FILMO_URL,
                      body=week.WEEK_HTML, status=200)
        responses.add(responses.GET,
                      re.compile(f'{scrapper.DetailScrapper.DETAIL_URL}.*'),
                      body=detail.FILM_DETAIL_HTML, status=200)

    @responses.activate
    def test_should_save_scrapped_films(self):
        scrapper.scrape()

        film = models.Film.objects.get(title='Werk ohne Autor')

        assert film

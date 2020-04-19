import responses

from django.test import TestCase
from rest_framework.test import APIClient
from requests.compat import urljoin

from api import scrapper
from api.test_files import week
from api.test_files import detail


class FilmViewTests(TestCase):

    def test_should_return_list_of_films(self):
        client = APIClient()

        response = client.get('/api/')

        assert response.status_code == 200
        assert response.json() == []


class WeekScrapperTests(TestCase):

    def setUp(self):
        responses.add(responses.GET, scrapper.WeekScrapper.FILMO_URL,
                      body=week.WEEK_HTML, status=200)

    @responses.activate
    def test_should_scrape_film_detail_links(self):
        week_scrapper = scrapper.WeekScrapper('2020-02-24')

        links = week_scrapper.scrape_detail_links()

        assert len(responses.calls) == 1
        assert '/web/ca/film/werk-ohne-autor' in links


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

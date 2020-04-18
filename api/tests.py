from django.test import TestCase
from rest_framework.test import APIClient


class FilmViewTests(TestCase):

    def test_should_return_list_of_films(self):
        client = APIClient()

        response = client.get('/api/')

        assert response.status_code == 200
        assert response.json() == []

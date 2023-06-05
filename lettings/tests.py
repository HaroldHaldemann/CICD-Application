from django.test import TestCase
from django.urls import reverse

from .models import Address, Letting


class LettingsTest(TestCase):

    def setUp(self):
        self.address = Address.objects.create(
            number=2,
            street="boulevard Carteret",
            city="Reims",
            state="Marne",
            zip_code=51100,
            country_iso_code="FRA"
        )
        self.letting = Letting.objects.create(title="Test Letting", address=self.address)

    def test_lettings_index(self):
        response = self.client.get(reverse('lettings:index'))
        assert response.status_code == 200
        assert b"<title>Lettings</title>" in response.content

    def test_letting_detail(self):
        response = self.client.get(reverse('lettings:letting', args=[1]))
        assert response.status_code == 200
        assert b"<title>Test Letting</title>" in response.content

    def test_lettings_models_str(self):
        assert str(self.address) == f'{self.address.number} {self.address.street}'
        assert str(self.letting) == self.letting.title

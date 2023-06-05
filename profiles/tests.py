from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Profile


class ProfilesTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="TestUser",
            password="password123",
            email="test_user@email.com"
        )
        self.profile = Profile.objects.create(user=self.user, favorite_city="Dublin")

    def test_profiles_index(self):
        response = self.client.get(reverse('profiles:index'))
        assert response.status_code == 200
        assert b"<title>Profiles</title>" in response.content

    def test_profile_detail(self):
        response = self.client.get(reverse('profiles:profile', args=["TestUser"]))
        assert response.status_code == 200
        assert b"<title>TestUser</title>" in response.content

    def test_profiles_models_str(self):
        assert str(self.profile) == self.user.username

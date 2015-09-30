from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from .views import avatar
from .generator import AvatarGenerator

class TestWithGravatar(TestCase):
    def setUp(self):
        self.userWithAvatar = User.objects.create_user(
            username='matt', email='matt@automattic.com', password='top_secret')
        self.userWithoutAvatar = User.objects.create_user(
            username='JAB', email='jab@axiome.io', password='top_secret')

    def test_gravatar_url(self):
		url = AvatarGenerator(self.userWithAvatar).get_avatar_url()
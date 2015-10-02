from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from PIL import Image, ImageDraw, ImageFont
from initial_avatars.views import avatar
from initial_avatars.generator import AvatarGenerator
import os

class TestAvatarGenerator(TestCase):
    def setUp(self):
        self.userA = User(username='JAB', email='jab@axiome.io', password='top_secret')
        self.genA = AvatarGenerator(self.userA, 80)
        self.userB = User(username='matt', first_name='matt', last_name='something',email='matt@automattic.com', password='top_secret')
        self.genB = AvatarGenerator(self.userB, 80)

    def test_text(self):
        self.assertEqual(self.genA.text(), 'J')
        self.assertEqual(self.genB.text(), 'MS')

    def test_font_size(self):
        self.assertEqual(self.genA.font_size(), 72)
        self.assertEqual(self.genB.font_size(), 64)
    
    def test_brightness(self):
        self.assertEqual(int(self.genA.brightness()), 222)
        self.assertEqual(int(self.genB.brightness()), 200)

    def test_background(self):
        self.assertEqual(self.genA.background(), (157, 242, 216))
        self.assertEqual(self.genB.background(), (208, 207, 63))

    def test_foreground(self):
        self.assertEqual(self.genA.foreground(), (0, 0 , 0))
        self.assertEqual(self.genB.foreground(), (0, 0 , 0))

    def test_position(self):
        image = Image.new('RGBA', (80, 80))
        draw = ImageDraw.Draw(image)
        self.assertEqual(self.genA.position(draw), (22,4))
        self.assertEqual(self.genB.position(draw), (8,6))

    def test_name(self):
        self.assertEqual(self.genA.name(), "JAB-80x80.jpg")
        self.assertEqual(self.genB.name(), "matt-80x80.jpg")

    def test_get_avatar_url(self):
        self.assertEqual(self.genA.get_avatar_url(), "django_initial_avatars.py/avatars/JAB/80x80/JAB-80x80.jpg")
        self.assertEqual(self.genB.get_avatar_url(), "https://secure.gravatar.com/avatar/c0ccdd53794779bcc07fcae7b79c4d80.jpg?s=80&amp;r=g&amp;d=mm")

    def test_get_avatar(self):
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(__file__), 'static', 'avatars' 'JAB', '80x80', 'JAB-80x80.jpg')))
        self.assertEqual(self.genA.get_avatar(), '<img class="initial-avatar" src="django_initial_avatars.py/avatars/JAB/80x80/JAB-80x80.jpg" width="80" height="80"/>')
        self.assertEqual(self.genB.get_avatar(),'<img class="gravatar" src="https://secure.gravatar.com/avatar/c0ccdd53794779bcc07fcae7b79c4d80.jpg?s=80&amp;r=g&amp;d=mm" width="80" height="80"/>')


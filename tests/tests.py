from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase
from django.core.files.storage import default_storage
from django.template import Context, Template
from PIL import Image, ImageDraw
from initial_avatars.generator import AvatarGenerator
from datetime import datetime


class TestAvatarGenerator(TestCase):

    TEMPLATE = Template("{% load initialavatar %} {% get_initial_avatar user %}")

    def setUp(self):
        self.userA = User.objects.create_user(
            username='JAB',
            email='admin@axiome.io',
            password='top_secret'
        )
        self.genA = AvatarGenerator(self.userA, 80)
        self.userB = User.objects.create_user(
            username='matt',
            first_name='matt',
            last_name='something',
            email='matt@automattic.com',
            password='top_secret'
        )
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
        self.assertEqual(self.genA.foreground(), (0, 0, 0))
        self.assertEqual(self.genB.foreground(), (0, 0, 0))

    def test_position(self):
        image = Image.new('RGBA', (80, 80))
        draw = ImageDraw.Draw(image)
        self.assertEqual(self.genA.position(draw), (22, 4))
        self.assertEqual(self.genB.position(draw), (8, 6))

    def test_name(self):
        self.assertEqual(self.genA.name(), "80x80.jpg")
        self.assertEqual(self.genB.name(), "80x80.jpg")

    def test_path(self):
        self.assertEqual(
            self.genA.path(),
            "avatars/1de33e9ce3bb61b6f82a27810590a785/80x80.jpg"
        )
        self.assertEqual(
            self.genB.path(),
            "avatars/579e0547027d49009b38d4ed91afb84d/80x80.jpg"
        )

    def test_get_avatar_url(self):
        self.assertEqual(
            self.genA.get_avatar_url(),
            "http://django-initial-avatars.py/avatars/1de33e9ce3bb61b6f82a27810590a785/80x80.jpg"
        )
        self.assertEqual(
            self.genB.get_avatar_url(),
            "https://secure.gravatar.com/avatar/c0ccdd53794779bcc07fcae7b79c4d80.jpg?s=80&amp;r=g&amp;d=mm"
        )

    def test_get_avatar(self):
        default_storage.delete(self.genA.path())
        self.assertFalse(default_storage.exists(self.genA.path()))
        self.assertEqual(
            self.genA.get_avatar(),
            '<img class="initial-avatar" src="http://django-initial-avatars.py/avatars/1de33e9ce3bb61b6f82a27810590a785/80x80.jpg" width="80" height="80"/>'
        )
        self.assertEqual(
            self.genB.get_avatar(),
            '<img class="gravatar" src="https://secure.gravatar.com/avatar/c0ccdd53794779bcc07fcae7b79c4d80.jpg?s=80&amp;r=g&amp;d=mm" width="80" height="80"/>'
        )
        self.assertTrue(default_storage.exists(self.genA.path()))

    def test_last_modified(self):
        self.assertIsInstance(self.genA.last_modification(), datetime)
        self.assertIsInstance(self.genB.last_modification(), datetime)

    def test_template_tags(self):
        renderedA = self.TEMPLATE.render(Context({'user': self.userA}))
        self.assertTrue(
            '<img class="initial-avatar" src="http://django-initial-avatars.py/avatars/1de33e9ce3bb61b6f82a27810590a785/80x80.jpg" width="80" height="80"/>',
            renderedA
        )
        renderedB = self.TEMPLATE.render(Context({'user': self.userB}))
        self.assertTrue(
            '<img class="gravatar" src="https://secure.gravatar.com/avatar/c0ccdd53794779bcc07fcae7b79c4d80.jpg?s=80&amp;r=g&amp;d=mm" width="80" height="80"/>',
            renderedB
        )
        renderedAnon = self.TEMPLATE.render(Context({'user': AnonymousUser()}))
        self.assertTrue(
            '<img src="" width="80" height="80"/>',
            renderedAnon
        )

    def test_view(self):
        responseA = self.client.get('/JAB/')
        self.assertEqual(responseA.status_code, 302)
        responseB = self.client.get('/matt/')
        self.assertEqual(responseB.status_code, 302)

    def test_anon_view(self):
        responseAnon = self.client.get('/anon/')
        self.assertEqual(responseAnon.status_code, 404)


class TestAvatarGeneratorNotDefault(TestCase):

    TEMPLATE = Template("{% load initialavatar %} {% get_initial_avatar user %}")

    def setUp(self):
        self.userA = User.objects.create_user(
            username='JAB',
            email='admin@axiome.io',
            password='top_secret'
        )
        self.genA = AvatarGenerator(self.userA, 150)
        self.userB = User.objects.create_user(
            username='matt',
            first_name='matt',
            last_name='something',
            email='matt@automattic.com',
            password='top_secret'
        )
        self.genB = AvatarGenerator(self.userB, 150)

    def test_text(self):
        self.assertEqual(self.genA.text(), 'J')
        self.assertEqual(self.genB.text(), 'MS')

    def test_font_size(self):
        self.assertEqual(self.genA.font_size(), 135)
        self.assertEqual(self.genB.font_size(), 120)

    def test_brightness(self):
        self.assertEqual(int(self.genA.brightness()), 222)
        self.assertEqual(int(self.genB.brightness()), 200)

    def test_background(self):
        self.assertEqual(self.genA.background(), (157, 242, 216))
        self.assertEqual(self.genB.background(), (208, 207, 63))

    def test_foreground(self):
        self.assertEqual(self.genA.foreground(), (0, 0, 0))
        self.assertEqual(self.genB.foreground(), (0, 0, 0))

    def test_position(self):
        image = Image.new('RGBA', (80, 80))
        draw = ImageDraw.Draw(image)
        self.assertEqual(self.genA.position(draw), (41, 9))
        self.assertEqual(self.genB.position(draw), (15, 12))

    def test_name(self):
        self.assertEqual(self.genA.name(), "150x150.jpg")
        self.assertEqual(self.genB.name(), "150x150.jpg")

    def test_path(self):
        self.assertEqual(
            self.genA.path(),
            "avatars/1de33e9ce3bb61b6f82a27810590a785/150x150.jpg"
        )
        self.assertEqual(
            self.genB.path(),
            "avatars/579e0547027d49009b38d4ed91afb84d/150x150.jpg"
        )

    def test_get_avatar_url(self):
        self.assertEqual(
            self.genA.get_avatar_url(),
            "http://django-initial-avatars.py/avatars/1de33e9ce3bb61b6f82a27810590a785/150x150.jpg"
        )
        self.assertEqual(
            self.genB.get_avatar_url(),
            "https://secure.gravatar.com/avatar/c0ccdd53794779bcc07fcae7b79c4d80.jpg?s=150&amp;r=g&amp;d=mm"
        )

    def test_get_avatar(self):
        default_storage.delete(self.genA.path())
        self.assertFalse(default_storage.exists(self.genA.path()))
        self.assertEqual(
            self.genA.get_avatar(),
            '<img class="initial-avatar" src="http://django-initial-avatars.py/avatars/1de33e9ce3bb61b6f82a27810590a785/150x150.jpg" width="150" height="150"/>'
        )
        self.assertEqual(
            self.genB.get_avatar(),
            '<img class="gravatar" src="https://secure.gravatar.com/avatar/c0ccdd53794779bcc07fcae7b79c4d80.jpg?s=150&amp;r=g&amp;d=mm" width="150" height="150"/>'
        )
        self.assertTrue(default_storage.exists(self.genA.path()))

    def test_last_modified(self):
        self.assertIsInstance(self.genA.last_modification(), datetime)
        self.assertIsInstance(self.genB.last_modification(), datetime)

    def test_template_tags(self):
        renderedA = self.TEMPLATE.render(Context({'user': self.userA}))
        self.assertTrue(
            '<img class="initial-avatar" src="http://django-initial-avatars.py/avatars/1de33e9ce3bb61b6f82a27810590a785/150x150.jpg" width="150" height="150"/>',
            renderedA
        )
        renderedB = self.TEMPLATE.render(Context({'user': self.userB}))
        self.assertTrue(
            '<img class="gravatar" src="https://secure.gravatar.com/avatar/c0ccdd53794779bcc07fcae7b79c4d80.jpg?s=80&amp;r=g&amp;d=mm" width="150" height="150"/>',
            renderedB
        )
        renderedAnon = self.TEMPLATE.render(Context({'user': AnonymousUser()}))
        self.assertTrue(
            '<img src="" width="150" height="150"/>',
            renderedAnon
        )

    def test_view(self):
        responseA = self.client.get('/JAB/150/')
        self.assertEqual(responseA.status_code, 302)
        responseB = self.client.get('/matt/150/')
        self.assertEqual(responseB.status_code, 302)
        responseAnon = self.client.get('/3/150/')
        self.assertEqual(responseAnon.status_code, 404)

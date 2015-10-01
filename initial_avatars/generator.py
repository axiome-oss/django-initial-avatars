try:
    from django_gravatar.helpers import get_gravatar_url, has_gravatar
except ImportError:
    pass
from django.utils.html import escape
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from django.db import connection
from PIL import Image, ImageDraw, ImageFont
from math import sqrt
from hashlib import md5
import os

GRAVATAR_DEFAULT_SIZE = getattr(settings, 'GRAVATAR_DEFAULT_SIZE', 80)

class AvatarGenerator(object):
    """
    inspired by https://github.com/4teamwork/ftw.avatar
    """

    def __init__(self, user, size=GRAVATAR_DEFAULT_SIZE):
        self.user = user
        self.size = size
        self.url = None
        self.css_class = None

    def name(self):
        return '{0}-{1}x{1}.jpg'.format(self.user.username, self.size)

    def path(self):
        if 'tenant_schemas' in settings.INSTALLED_APPS:
            return os.path.join(connection.tenant.schema_name, 'avatars', self.user.username, '{0}x{0}'.format(self.size), self.name())
        else:
            return os.path.join('avatars', self.user.username, '{0}x{0}'.format(self.size), self.name())

    def font(self):
        font_path = os.path.join(os.path.dirname(__file__), 'font', 'UbuntuMono-B.ttf')
        font_size = int(self.size * (1 - 0.1 * len(self.text())))
        return ImageFont.truetype(font_path, size=font_size)

    def background(self):
        hash = md5(self.user.username).hexdigest()
        hash_values = (hash[:8], hash[8:16], hash[16:24])
        background = tuple(int(value, 16)%256 for value in hash_values)
        return background

    def foreground(self):
        """
        explanation of the formula on http://www.nbdtech.com/Blog/archive/2008/04/27/Calculating-the-Perceived-Brightness-of-a-Color.aspx
        """
        rCoef = 0.241
        gCoef = 0.691
        bCoef = 0.068
        background = self.background()
        brightness = sqrt(rCoef * background[0]**2 + gCoef * background[1]**2 + bCoef * background[2]**2)
        if brightness > 130:
            return (0, 0, 0)
        else:
            return (255, 255, 255)

    def position(self, draw):
        text_width, text_height = draw.textsize(self.text(), font=self.font())
        left = ((self.size - text_width) / 2)
        top = ((self.size - text_height) / 4)
        return left, top

    def text(self):
        if self.user.first_name and self.user.last_name:
            initial = self.user.first_name[:1].upper() + self.user.last_name[:1].upper()
        else:
            initial = self.user.username[:1].upper()
        return initial

    def genavatar(self):
        image = Image.new('RGBA', (self.size, self.size), self.background())
        draw = ImageDraw.Draw(image)
        tmpPath = os.path.join('/tmp/', self.name())
        w, h = self.position(draw)
        draw.text((w, h), self.text(), fill=self.foreground(), font=self.font())
        image.save(tmpPath)
        try:
            f = open(tmpPath)
            django_file = File(f)
            saved_file = default_storage.save(self.path(), django_file)
            os.remove(tmpPath)
            return default_storage.url(self.path())
        except Exception, e:
            print e

    def get_avatar_url(self):
        try:
            if has_gravatar(self.user.email):
                self.css_class = "gravatar"
                url = escape(get_gravatar_url(email=self.user.email, size=self.size))
                return url
        except NameError:
            pass
        self.css_class = "initial-avatar"
        if default_storage.exists(self.path()):
            url = default_storage.url(self.path())
        else:
            url = self.genavatar()
        return url

    def get_avatar(self):
        self.url = self.get_avatar_url()
        return '<img class="{css_class}" src="{src}" width="{width}" height="{height}"/>'.format(css_class=self.css_class, src=self.url, width=self.size, height=self.size)

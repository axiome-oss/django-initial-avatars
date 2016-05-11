# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import unicode_literals
import os
import re
try:
    from django_gravatar.helpers import get_gravatar_url, has_gravatar
except ImportError:
    pass
from django.utils.html import escape
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import default_storage, get_storage_class
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from math import sqrt
from hashlib import md5
from datetime import datetime
from random import choice
from .utils import AVATAR_SHAPE_SETTINGS, AVATAR_FOREGROUND_COLORS, AvatarShapeException, AvatarForegroundColorException
from .models import Background
from .compat import urlopen

GRAVATAR_DEFAULT_SIZE = getattr(settings, 'GRAVATAR_DEFAULT_SIZE', 80)
AVATAR_SHAPE = getattr(settings, 'AVATAR_DEFAULT_SHAPE', 'square')
AVATAR_STORAGE_FOLDER = getattr(settings, 'AVATAR_STORAGE_FOLDER', 'avatars')
AVATAR_HIGH_RESOLUTION = getattr(settings, 'AVATAR_HIGH_RESOLUTION', False)
AVATAR_COLORS = getattr(settings, 'AVATAR_COLORS', False)

try:
    AVATAR_DEFAULT_FOREGROUND = AVATAR_FOREGROUND_COLORS[settings.AVATAR_DEFAUL_TEXT_COLOR]
except KeyError:
    raise AvatarForegroundColorException
except AttributeError:
    pass

try:
    AVATAR_STORAGE_BACKEND = get_storage_class(settings.AVATAR_STORAGE_BACKEND)()
except AttributeError:
    AVATAR_STORAGE_BACKEND = default_storage


class AvatarGenerator(object):
    """
        inspired by https://github.com/4teamwork/ftw.avatar
    """

    def __init__(self, user, size=GRAVATAR_DEFAULT_SIZE, shape=AVATAR_SHAPE):
        self.user = user
        self.work_size = size * 10
        self.size = size
        self.shape = shape
        try:
            self.image_format = AVATAR_SHAPE_SETTINGS[shape]['image_format']
            self.content_type = AVATAR_SHAPE_SETTINGS[shape]['content_type']
        except KeyError:
            raise AvatarShapeException
        self.css_class = None
        self.url = None
        if AVATAR_HIGH_RESOLUTION:
            self.high_res_url = None

    def name(self, high_res=False):
        """
            returns the name of the img file
        """
        if high_res:
            name = "{0}x{0}_{1}@2x.{2}".format(self.size, self.shape, self.image_format)
        else:
            name = '{0}x{0}_{1}.{2}'.format(self.size, self.shape, self.image_format)
        return name

    def path(self, high_res=False):
        """
            returns the path of the img file
        """
        user_hash = md5(os.path.join(self.user.username, self.user.first_name, self.user.last_name).encode('utf-8')).hexdigest()
        user_path = os.path.join(AVATAR_STORAGE_FOLDER, user_hash, self.name(high_res))
        return user_path

    def font_size(self):
        """
            returns the size of the font calculated according to the size of requested avatar
        """
        font_size = int(self.work_size * (1 - 0.1 * len(self.text())))
        return font_size

    def font(self):
        """
            returns an ImageFont object with the font used to generate the avatar
        """
        font_path = os.path.join(os.path.dirname(__file__), 'font', 'UbuntuMono-B.ttf')
        font_size = self.font_size()
        return ImageFont.truetype(font_path, size=font_size)

    def choose_random_background(self):
        try:
            backgroundObject = Background.objects.get(user=self.user)
            background = (backgroundObject.R, backgroundObject.G, backgroundObject.B)
        except Background.DoesNotExist:
            background = choice(AVATAR_COLORS)
            Background.objects.create(user=self.user, R=background[0], G=background[1], B=background[2])
        return background

    def background(self):
        """
            returns the background color based on the username md5
        """
        if AVATAR_COLORS:
            background = self.choose_random_background()
        else:
            hash = md5(self.user.username.encode('utf-8')).hexdigest()
            hash_values = (hash[:8], hash[8:16], hash[16:24])
            background = tuple(int(value, 16) % 256 for value in hash_values)
        return background

    def brightness(self):
        """
            returns the brightness of the background color
            explanation of the formula on http://www.nbdtech.com/Blog/archive/2008/04/27/Calculating-the-Perceived-Brightness-of-a-Color.aspx
        """
        rCoef = 0.241
        gCoef = 0.691
        bCoef = 0.068
        background = self.background()
        brightness = sqrt(rCoef * background[0]**2 + gCoef * background[1]**2 + bCoef * background[2]**2)
        return brightness

    def foreground(self):
        """
            returns black or white according to the brightness
        """
        try:
            return AVATAR_DEFAULT_FOREGROUND
        except NameError:
            brightness = self.brightness()
            if brightness > 130:
                return (0, 0, 0)
            else:
                return (255, 255, 255)

    def position(self, draw):
        """
            returns the position where the initials must be printed
        """
        text_width, text_height = draw.textsize(self.text(), font=self.font())
        left = ((self.work_size - text_width) / 2)
        top = ((self.work_size - text_height) / 4)
        return left, top

    def text(self):
        """
            returns the text to be printed on the avatar
            first letter of first_name and last_name if they exists
            first letter of the username if not

            Attempts to find first capital letter of last name. This supports
            names such as "Alexandre da Rocha" by using the correct form "AR".
        """
        if self.user.first_name and self.user.last_name:
            initial = self.user.first_name[:1].upper()

            match = re.search(r'[A-Z]', self.user.last_name)
            if match:
                # Use first capital letter
                initial += match.group()
            else:
                # No capitals found; just use first letter
                initial += self.user.last_name[:1].upper()
        else:
            initial = self.user.username[:1].upper()
        return initial

    def last_modification(self):
        """
            returns the avatar last_modification
        """
        try:
            if has_gravatar(self.user.email):
                info = urlopen(get_gravatar_url(email=self.user.email, size=self.size)).info()
                return datetime.strptime(info['Last-Modified'], "%a, %d %b %Y %H:%M:%S GMT")
        except NameError:
            pass
        if AVATAR_STORAGE_BACKEND.exists(self.path()):
            try:
                return AVATAR_STORAGE_BACKEND.modified_time(self.path())
            except AttributeError:
                return timezone.now()
        else:
            return None

    def genavatar(self):
        if self.shape == 'square':
            return self.gen_image_avatar(self.background())
        elif self.shape == 'circle':
            return self.gen_image_avatar((255, 0, 0, 0))
        else:
            raise AvatarShapeException

    def gen_image_avatar(self, background):
        work_image = Image.new('RGBA', (self.work_size, self.work_size), background)
        draw = ImageDraw.Draw(work_image)
        if self.shape == 'circle':
            draw.ellipse((0, 0, self.work_size, self.work_size), fill=self.background())
        w, h = self.position(draw)
        draw.text((w, h), self.text(), fill=self.foreground(), font=self.font())
        image = work_image.resize((self.size, self.size), resample=Image.BILINEAR)
        self.url = self.save_avatar(image)
        if AVATAR_HIGH_RESOLUTION:
            high_res_image = work_image.resize((self.size * 2, self.size * 2), resample=Image.BILINEAR)
            self.high_res_url = self.save_avatar(high_res_image, high_res=True).decode('utf-8')
        return self.url

    def save_avatar(self, image, high_res=False):
        image_io = BytesIO()
        image.save(image_io, format=self.content_type)
        image_io.seek(0, os.SEEK_END)
        image_io_length = image_io.tell()
        image_name = self.name(high_res)
        try:
            django_file = InMemoryUploadedFile(image_io, None, image_name, 'image/{0}'.format(self.content_type.lower()), image_io_length, None)
            AVATAR_STORAGE_BACKEND.save(self.path(high_res), django_file)
            return AVATAR_STORAGE_BACKEND.url(self.path(high_res))
        except Exception as e:
            raise e

    def get_avatar_url(self):
        """
            returns the url of the avatar on the storage backed
        """
        try:
            if has_gravatar(self.user.email):
                self.css_class = "gravatar"
                self.url = escape(get_gravatar_url(email=self.user.email, size=self.size))
                return self.url
        except NameError:
            pass

        self.css_class = "initial-avatar"
        if AVATAR_STORAGE_BACKEND.exists(self.path()):
            self.url = AVATAR_STORAGE_BACKEND.url(self.path())
        else:
            self.url = self.genavatar()
        if AVATAR_HIGH_RESOLUTION:
            self.high_res_url = AVATAR_STORAGE_BACKEND.url(self.path(high_res=True))
            return self.url, self.high_res_url
        return self.url

    def get_avatar(self):
        """
            returns an html img tag with the avatar
        """
        self.get_avatar_url()
        if AVATAR_HIGH_RESOLUTION:
            return '<img class="{css_class}" src="{src}" srcset="{src} 1x, {high_res_src} 2x" width="{width}" height="{height}"/>'.format(
                css_class=self.css_class,
                src=self.url,
                high_res_src=escape(self.high_res_url),
                width=self.size,
                height=self.size
            )
        return '<img class="{css_class}" src="{src}" width="{width}" height="{height}"/>'.format(
            css_class=self.css_class,
            src=self.url,
            width=self.size,
            height=self.size
        )

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django import template
from ..generator import GRAVATAR_DEFAULT_SIZE, AVATAR_SHAPE
from ..utils import get_avatar_backend

register = template.Library()


@register.simple_tag(name='get_initial_avatar')
def get_initial_avatar(user_or_email, size=GRAVATAR_DEFAULT_SIZE, shape=AVATAR_SHAPE):
    """ Builds an avatar <img> tag from an user or email """

    if hasattr(user_or_email, 'email'):
        user = user_or_email
        email = user.email
    else:
        email = user_or_email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return mark_safe('<img src="" width="{width}" height="{height}"/>'.format(width=size, height=size))

    avatar_backend = get_avatar_backend()
    return mark_safe(avatar_backend(user, size=int(size), shape=shape).get_avatar())
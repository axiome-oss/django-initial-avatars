from django.contrib.auth.models import User
from django import template
from initial_avatars.generator import AvatarGenerator

register = template.Library()

@register.simple_tag(name='get_initial_avatar')
def get_initial_avatar(user_or_email, size=GRAVATAR_DEFAULT_SIZE):
    """ Builds an avatar <img> tag from an user or email """

    if hasattr(user_or_email, 'email'):
        email = user_or_email.email
    else:
        email = user_or_email
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExists:
        return "<img>src="" width="{width}" height="{height}"/>".format(width=size, height=size)
    return AvatarGenerator(user, size=int(size)).get_avatar()

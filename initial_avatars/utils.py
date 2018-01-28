from django.conf import settings
from importlib import import_module


class AvatarShapeException(BaseException):
    pass


class AvatarForegroundColorException(BaseException):
    pass


def get_avatar_backend():
    backend_name = getattr(settings, 'AVATAR_GENERATOR_BACKEND', 'initial_avatars.generator.AvatarGenerator')
    backend_module_name, backend_cls_name = backend_name.rsplit('.', 1)
    backend_module = import_module(backend_module_name)
    backend_class = getattr(backend_module, backend_cls_name)
    return backend_class

AVATAR_SHAPE_SETTINGS = {
    'circle': {
        'image_format': 'png',
        'content_type': 'PNG',
        'color_channels': 'RGBA'
    },
    'square': {
        'image_format': 'jpg',
        'content_type': 'JPEG',
        'color_channels': 'RGB'
    }
}

AVATAR_FOREGROUND_COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0)
}

class AvatarShapeException(BaseException):
    pass

class AvatarForegroundColorException(BaseException):
    pass


AVATAR_SHAPE_SETTINGS = {
    'circle': {
        'image_format': 'png',
        'content_type': 'PNG'
    },
    'square': {
        'image_format': 'jpg',
        'content_type': 'JPEG'
    }
}

AVATAR_FOREGROUND_COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0)
}

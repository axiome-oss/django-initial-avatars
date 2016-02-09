class AvatarShapeException(BaseException):
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

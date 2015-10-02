SECRET_KEY = 'fake-key'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'django_initial_avatars.sqlite'
    }
}
INSTALLED_APPS = [
    'initial_avatars',
    'django_gravatar',
]
MEDIA_URL = 'django_initial_avatars.py/'
MEDIA_ROOT = 'tests/static'
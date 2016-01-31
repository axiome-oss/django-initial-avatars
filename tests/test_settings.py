from __future__ import unicode_literals
import os

SECRET_KEY = 'fake-key'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST_NAME': os.path.join(os.path.dirname(__file__), 'django_initial_avatars.sqlite'),
    }
}
INSTALLED_APPS = [
	'django.contrib.contenttypes',
	'django.contrib.auth',
    'initial_avatars',
    'django_gravatar',
]
MEDIA_URL = 'http://django-initial-avatars.py/'
MEDIA_ROOT = 'tests/static'
ROOT_URLCONF = 'initial_avatars.urls'

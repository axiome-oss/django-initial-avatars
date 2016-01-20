django-initial-avatars

======================

.. image:: https://badge.fury.io/py/django-initial-avatars.svg
    :target: https://badge.fury.io/py/django-initial-avatars

django-initial-avatars is a simple Django app which generates avatars based on username and initials. If django_gravatar is installed, user's gravatar is preferred.

Examples
-----------

* API endpoint
.. image:: https://metod-site.s3.amazonaws.com/media/25/initial_avatars.png
    :target: http://www.metod.io/fr/blog/2015/12/02/release-django-initial-avatars/
    :alt: example of django-initial-avatars on Metod
    
* Template tag
.. image:: https://metod-site.s3.amazonaws.com/media/25/initial_avatars_email.png
    :target: http://www.metod.io/fr/blog/2015/12/02/release-django-initial-avatars/
    :alt: example of django-initial-avatars in Metod emails

Dependencies
------------

Generating avatars requires a `Pillow` installation with `freetype` support.

``freetype`` can easily be installed on ubuntu with::
	
	$ sudo aptitude install libfreetype6-dev

or on OS X with `homebrew`::

    $ brew install freetype

After installing ``freetype`` Pillow may need to be rebuilt.

Font licensing
--------------

For generating the avatar the font ``Ubuntu Monospace`` is used.
The font is licensed under the Ubuntu Font Licence, see the
`License <http://font.ubuntu.com/licence/>`_

Quick start
-----------
1. install app requirements

2. install django-initial-avatars through pip::

    pip install django-initial-avatars

3. If you want to use gravatar for users who have one, install django-gravatar2::

    pip install django-gravatar2

4. Add "django-initial-avatars" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'initial_avatars',
        ['django_gravatar',]
    )

5. Include the django-initial-avatar URLconf in your project urls.py like this::

    url(r'^avatar/', include('initial_avatars.urls')),

6. Launch development server::

	python manage.py runserver

7. Each user has now an endpoint for his avatar::

	localhost:8000/avatar/user_id/[size/]

8. In your templates, use::

    {% load initialavatar %}

    {% get_initial_avatar user [size] %}

    {% get_initial_avatar user.email [size] %}

Settings
--------------

You can define a setting to use a specific storage backend instead of the default one::

        AVATAR_STORAGE_BACKEND = 'myproject.custom_storages.AvatarStorage'

Tests
--------------

Django-initial-avatars is provided with tests, they require django-gravatar2

You can launch them in the virtualenv like this::

        python runtests.py

It might happen that a calculated position fails because of a minor difference in the result, don't care about it.

Contributions
--------------

Contributions are welcome ! Feel free to write an issue for any feedback you have or send a pull request on `Github <https://github.com/axiome-oss/django-initial-avatars>`_

Used on
--------------

* `Metod <http://www.metod.io/>`_
* Add your website here !

=====
django-initial-avatars
=====

django-initial-avatars is a simple Django app which generates avatars based on username and initials. If django_gravatar is installed, user gravatar is preferred.

Dependencies
------------

Generating avatars requires a `Pillow`_ (or PIL) installation with `freetype`_ support.

``freetype`` can easily be installed on ubuntu with _::
	
	$ sudo aptitude install libfreetype6-dev

or on OS X with `homebrew`_::

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

2. If you want to use gravatar for users who have one, install django-gravatar2::

    pip install django-gravatar2

3. Add "django-initial-avatars" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'initial_avatars',
        ['django_gravatar',]
    )

4. Include the django-initial-avatar URLconf in your project urls.py like this::

    url(r'^avatar/', include('initial_avatars.urls')),

5. Launch development server::

	python manage.py runserver

6. Each user has now an endpoint for his avatar::

	localhost:8000/avatar/user[/size]

7. In your templates, use::

    {% load initial_avatars %}

    {% get_initial_avatar user [size] %}

or

    {% get_initial_avatar user.email [size] %}


8. To-do:

	Write Tests

	add settings ?


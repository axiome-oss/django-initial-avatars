django-initial-avatars

======================

.. image:: https://badge.fury.io/py/django-initial-avatars.svg  
    :target: https://badge.fury.io/py/django-initial-avatars
.. image:: https://travis-ci.org/axiome-oss/django-initial-avatars.svg?branch=master
    :target: https://travis-ci.org/axiome-oss/django-initial-avatars

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

Make sure the following packet are installed on your system to enable PNG and JPG support on Pillow::

    $ sudo aptitude install libjpeg-dev zlib1g-dev libpng12-dev

Pillow may need to be rebuilt after installing the libraries.

Font licensing
--------------

The font ``Ubuntu Monospace`` is used to generate the avatar.
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

    {% get_initial_avatar user [size] ['shape'] %}

    {% get_initial_avatar user.email [size] ['shape'] %}


Settings
-----------

A few settings are at your disposal

* AVATAR_STORAGE_BACKEND allows you to use a custom storage backend instead of the default one::

    AVATAR_STORAGE_BACKEND = 'myproject.custom_storages.AvatarStorage'

* AVATAR_STORAGE_FOLDER allows you to customize the root folder on the storage backend, default to 'avatars'::

    AVATAR_STORAGE_FOLDER = 'myfolder'

* AVATAR_DEFAULT_SHAPE allows you to choose the default shape of the image, possible options are 'circle' or 'square', default to 'square'

  More shapes can be easily addded, just open an issue on github::

    AVATAR_DEFAULT_SHAPE = 'circle'

* GRAVATAR_DEFAULT_SIZE allows you to choose the default size of the image, setting name used for compatibility with django_gravatar, default to '80'::

    GRAVATAR_DEFAULT_SIZE = 100


Experimental settings
------------
Those feature are available but miss tests, contributions would be appreciated :)

* AVATAR_HIGH_RESOLUTION can be used to display retina ready avatas, default to False::

    AVATAR_HIGH_RESOLUTION = True

* AVATAR_COLORS can be used to randomly choose a color from a tuple of pre-defined colors at first avatar generation, no default::

    AVATAR_COLORS = ((37, 114, 221), (26, 193, 255),)

* AVATAR_DEFAULT_FOREGROUND can be used to define a default color to the foreground, 'black' and 'white' available, no default. I advise not to use it without AVATAR_COLORS::

    AVATAR_DEFAULT_FOREGROUND = 'white'

* AVATAR_GENERATOR_BACKEND can be used to extend the avatar generator and adjust it to your needs, especially for font customization. Refer to initial_avatars/generator.py for more information::

    AVATAR_GENERATOR_BACKEND = 'my_project.avatar_backend.MyAvatarBackend'


.. code-block:: python
    from initial_avatars.generator import AvatarGenerator
    from PIL import ImageFont
    import os
    class MyAvatarBackend(AvatarGenerator):
         def font(self):
            font_path = '/path/to/your/font'
            font_size = self.font_size()
            return ImageFont.truetype(font_path, size=font_size)



Tests
--------------

Django-initial-avatars is provided with tests, they require django-gravatar2 and tox

You can launch them in the virtualenv like this::

        tox

It might happen that a calculated position fails because of a minor difference in the result, don't care about it.

Contributions
--------------

Contributions are welcome ! Feel free to write an issue for any feedback you have or send a pull request on `Github <https://github.com/axiome-oss/django-initial-avatars>`_

Used on
--------------

* `Metod <http://www.metod.io/>`_
* Add your website here !

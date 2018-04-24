import os
from setuptools import setup
from initial_avatars import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-initial-avatars',
    version=__version__,
    packages=['initial_avatars', 'initial_avatars.templatetags'],
    include_package_data=True,
    license='BSD License',
    description='A simple Django app to get avatars based on username and initials if no gravatars is associated with the email address.',
    keywords='django avatar gravatar',
    long_description=open('README.rst').read(),
    url='https://github.com/axiome-oss/django-initial-avatars',
    author='Mathieu Requillart',
    author_email='mathieu.requillart@gmail.com',
    install_requires=[
        'Pillow',
        'Django',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    extras_require={
        'gravatar': ['django-gravatar2>=1.3.0'],
    },
    zip_safe=False,
    test_suite="runtests.runtests",
)

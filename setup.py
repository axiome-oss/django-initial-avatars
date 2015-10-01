import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-initial-avatars',
    version='0.2',
    packages=['initial_avatars', 'initial_avatars.templatetags'],
    include_package_data=True,
    license='BSD License', 
    description='A simple Django app to get avatars based on username and initials if no gravatars is associated to the email address.',
    keywords='django gravatar initial avatar',
    long_description=open('README.rst').read(),
    url='https://github.com/axiome-oss/django-initial-avatars',
    author='Mathieu Requillart',
    author_email='mrequillart@axiome.io',
    install_requires=[
        'Pillow',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    extras_require={'gravatar': ['django-gravatar2>=1.3.0'],
    },
    zip_safe = False,
)

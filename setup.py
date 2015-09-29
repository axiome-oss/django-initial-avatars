import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-intial-avatars',
    version='0.1',
    packages=['initial_avatars', 'initial_avatars.templatetags'],
    include_package_data=True,
    license='BSD License', 
    description='A simple Django app to get username based initial avatars, or gravatars.',
    keywords='django gravatar initial avatar',
    long_description=open('README.rst').read(),
    url='http://www.example.com/',
    author='Mathieu Requillart',
    author_email='mrequillart@axiome.io',
    install_requires=[
        'django-gravatar2',
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
    zip_safe = False,
)

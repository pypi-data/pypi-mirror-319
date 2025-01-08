#!/usr/bin/env python
import sys
from admin_honeypot import __version__, __description__, __license__

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='django-admin-honeypot-killua8p',
    version=__version__,
    description=__description__,
    long_description=open('./README.rst', 'r').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    keywords='django admin honeypot trap',
    author='Derek Payton',
    author_email='derek.payton@gmail.com',
    maintainer='killua8p',
    maintainer_email='killua8p@gmail.com',
    url='https://github.com/killua8p/django-admin-honeypot',
    download_url='https://github.com/killua8p/django-admin-honeypot/tarball/v%s' % __version__,
    license=__license__,
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'django-ipware',
    ]
)

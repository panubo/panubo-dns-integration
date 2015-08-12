#!/usr/bin/env python

from setuptools import setup

setup(
    name='panubo-dns-integration',
    version='0.0.1',
    author='Volt Grid Pty Ltd',
    author_email='andrew@voltgrid.com',
    license='MIT',
    description='Bind DNS integration using CouchDB',
    long_description=open('README.md').read(),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    url='https://github.com/panubo/panubo-dns-integration',
    scripts=['sync.py'],
    zip_safe=False,
    install_requires=['click==4.1', 'couchdbkit==0.6.5', 'requests==2.3.0',],
    tests_require=['pytest', 'pytest-capturelog'],
)

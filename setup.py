#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages

setup(name = "tweepy",
      version = "2.0",
      description = "Twitter API Library",
      license = "MIT",
      author = "Joshua Roesslein",
      url = "http://github.com/tweepy/tweepy",
      keywords = "twitter library",
      packages = find_packages(),
      requires = [
          'requests',
      ],
      test_suite = 'nose.collector',
      tests_require = ['nose'],
      zip_safe = True
)


# -*- coding: utf-8 -*-
import os
import codecs
from setuptools import setup

def read(fname):
    try:
        with codecs.open(fname, 'r', 'utf-8') as f:
            return f.read()
    except IOError:
        return ''

version=read(os.path.join('bopomofo','__version__.py')).strip().split('=')[-1].strip("' ")

setup(name='bopomofo',
      version=version,
      description='Translate chinese word to bopomofo',
      url='https://github.com/antfu/bopomofo',
      author='Anthony Fu',
      author_email='anthonyfu117@hotmail.com',
      license='MIT',
      long_description=read('README.rst'),
      packages=['bopomofo'],
      install_requires=['xpinyin'],

      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules',

          'License :: OSI Approved :: MIT License',

          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5'
      ],)

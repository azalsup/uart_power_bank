try:
    # Try using ez_setup to install setuptools if not already installed.
    from ez_setup import use_setuptools
    use_setuptools()
except ImportError:
    # Ignore import error and assume Python 3 which already has setuptools.
    pass

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

from setuptools import setup, find_packages

classifiers = ['Development Status :: 4 - Beta',
               'Operating System :: POSIX :: Linux',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(name              = 'upbc',
      version           = '0.2.0',
      author            = 'azalsup',
      author_email      = 'azalsup@gmail.com',
      description       = 'Library for accessing a power bank',
      license           = 'XXX',
      classifiers       = classifiers,
      url               = '[TODO] githun ??',
      dependency_links  = ['https://github.com/pyserial/pyserial'],
      install_requires  = ['pyserial>=1.0.13'],
      packages          = find_packages(),

      long_description = long_description,
      long_description_content_type = 'text/markdown')

"""Project setup script."""

import os
import subprocess

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    'requests',
  ]

setup(name='CTFR',
      version='0.0',
      description='Get Transparency logs for getting HTTPS websites subdomains ',
      long_description=README,
      classifiers=[
      ],
      author='',
      author_email='',
      url='',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      entry_points="""\
      [console_scripts]
      caca = console:main
      """,
      )
from setuptools import setup

# read the contents of your README file
from os import path
import re


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


with open(path.join(this_directory, 'version.py'), encoding='latin1') as fp:
    #long_description = fp.read()
    try:
        match = re.search('.*\"(.*)\"', fp.readline())
        print(match)
        version = match.group(1)
    except IndexError:
        raise RuntimeError('Unable to determine version.')

setup(name='cbpi4-buzzer',
      version=version,
      description='CraftBeerPi4 Buzzer Plugin',
      author='Alexander Vollkopf',
      author_email='avollkopf@web.de',
      url='https://github.com/PiBrewing/cbpi4-buzzer',
      license='GPLv3',
      keywords='globalsettings',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4-buzzer': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4-buzzer'],
      install_requires=[
      'cbpi4>=4.1.10'
      ],
      long_description=long_description,
      long_description_content_type='text/markdown'
     )

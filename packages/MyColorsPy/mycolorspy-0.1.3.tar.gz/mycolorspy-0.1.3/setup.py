from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='MyColorsPy',
  version='0.1.3',
  author='VolodyaHoi',
  author_email='i4masyrov@gmail.com',
  description='Module for using color in win command line or terminal.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/VolodyaHoi/MyColorsPy',
  packages=['MyColorsPy']
)
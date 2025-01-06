from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='scipystat',
  version='0.0.5',
  description='This is the simplest module for quick work with files.',
  license='MIT',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com',
  packages=find_packages(),
  keywords='files terver '
)

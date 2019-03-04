import io
from setuptools import find_packages, setup


def long_description():
    with io.open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
    return readme

setup(name='featselector',
      version='0.1.0',
      description='Pythonic Features Selector by Statistics and Model',
      long_description=long_description(),
      long_description_content_type="text/markdown",

      url='https://github.com/xiaorancs/feature-select',
      author='Ran Xiao',
      author_email="xiaoranone@gmail.com",

      license='MIT',
      packages=find_packages(),
      platforms = "Linux",

      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          ],
      install_requires = ['requires']
      )

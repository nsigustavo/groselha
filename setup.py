# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '0.0.1'

setup(name='groselha',
      version=version,
      description="Javascript Page Templates are an HTML/XML generation tool.",
      long_description=open("README.rst").read(),
      classifiers=[],
      keywords='',
      author='Time de busca da globo.com',
      author_email='busca@corp.globo.com',
      url='http://busca.globo.com/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'testes']),
      include_package_data=True,
      zip_safe=True,
      install_requires=['BeautifulSoup'],
)
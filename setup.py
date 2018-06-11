#!/usr/bin/env python

"""dcosdev project"""
from setuptools import find_packages, setup

REQUIRES = [
    'yml',
    'docopt==0.6.2',
    'docker',
    'minio',
    'requests',
    'boto3'
]
print(find_packages())
setup(name='dcosdev',
      version='0.0.1',
      description='short description',
      long_description='long description',
      platforms=["Linux"],
      author="...",
      author_email="...",
      url="...",
      license="Apache 2",
      packages=find_packages(),
      entry_points={
        'console_scripts': [
            'dcosdev=dcosdev.dcosdev:main',
        ],
      },
      install_requires=REQUIRES,
      zip_safe=False,
      include_package_data=True,
      )

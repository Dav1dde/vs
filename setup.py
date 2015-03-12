#!/usr/bin/env python2
# -*- coding: utf8 -*-

from setuptools import setup, find_packages


if __name__ == '__main__':
    setup(
        name='vs',
        version='0.1.0a0',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'flask',
            'flask-restful',
            'itsdangerous',
            'redis'
        ],
        entry_points={
            'console_scripts': [
                'vs = vs.__main__:main'
            ]
        }
    )

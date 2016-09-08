#!/usr/bin/env python3

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(
    name='passotp',
    version='0.1.0',
    author='Felipe Lerena',
    description='An TOTP cli for Pass',
    author_email='felipelerena@gmail.com',
    packages=['passotp'],
    scripts=[],
    url='https://github.com/felipelerena/passotp/',
    license='GPLv3',
    long_description="",
    install_requires=[
        "clipboard",
        "pyOTP"
    ],
    entry_points={
        'console_scripts': [
            'passotp = passotp.__init__:main',
        ]
    },
)

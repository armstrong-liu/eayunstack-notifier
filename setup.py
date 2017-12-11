#!/usr/bin/env python
# coding=utf-8
# setuptools with find_packages.
from setuptools import setup, find_packages

setup(
    name="eayunstack-notifier",
    version="0.0.1",
    packages=find_packages(),
    author='eayun',
    author_email='eayunstack@eayun.com',
    description='Eayunstack Notifier Tool',
    license='GPLv3',
    keywords='eayunstack-notifier',

    entry_points={
            'console_scripts': [
                        'eayunstack-notifier = eayunstack_notifier.cmd.agent_notifier:main',
                    ]})

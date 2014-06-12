# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import codecs
import os
from setuptools import setup, find_packages
import sys
from version import get_version

version = get_version()

with codecs.open('README.txt', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.txt"), encoding='utf-8') as f:
    long_description += '\n' + f.read()

requires = [
        'zope.browsermenu',
        'zope.browserpage',
        'zope.browserresource',
        'zope.cachedescriptors',
        'zope.component',
        'zope.formlib',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
        'zope.tal',
        'zope.tales',
        'Zope2',
        'gs.content.form.base',  # For the messsage content provider.
        'gs.content.js.jquery.base',
        'gs.content.layout',
        'gs.core',
        'gs.group.member.email.base',
        'gs.profile.base',
        'gs.profile.email.base',
        'gs.profile.email.verify',
        'Products.CustomUserFolder',
    ]
if (sys.version_info < (3, 4)):
    requires += ['setuptools', ]

setup(name='gs.profile.email.settings',
    version=version,
    description="Update email address settings on GroupServer.",
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Environment :: Web Environment",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: Zope Public License',
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
    keywords='profile, email, email address, settings,groupserver',
    author='Alice Murphy',
    author_email='alice@onlinegroups.net',
    maintainer='Michael JasonSmith',
    maintainer_email='mpj17@onlinegroups.net',
    url='https://source.iopen.net/groupserver/gs.profile.email.settings/',
    license='ZPL 2.1',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['gs', 'gs.profile', 'gs.profile.email'],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points="""
    # -*- Entry points: -*-
    """,)

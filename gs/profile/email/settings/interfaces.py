# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014, 2015 OnlineGroups.net and Contributors.
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
from __future__ import unicode_literals
from zope.interface import Interface
from zope.schema import ASCIILine
from gs.profile.email.base.emailaddress import NewEmailAddress, EmailAddress


class IAddAddress(Interface):
    email = NewEmailAddress(
        title='New email address',
        description='The email address to add',
        required=True)


class IDeleteAddress(Interface):
    email = EmailAddress(
        title='Email address',
        description='The email address to remove',
        required=True)


class IPreferAddress(Interface):
    email = EmailAddress(
        title='Email address',
        description='The email address to prefer (set as default delivery)',
        required=True)


class IDemoteAddress(Interface):
    email = EmailAddress(
        title='Email address',
        description='The email address to demote (set as non-default delivery)',
        required=True)


class IResendVerification(Interface):
    email = EmailAddress(
        title='Email address',
        description='The email address to send the verification message to',
        required=True)


class IGroupSettingsContentProvider(Interface):
    'The interface that the group email-settings content provider uses'
    pageTemplateFileName = ASCIILine(
        title='Page template file name',
        description='The page template for the group-settings',
        default=b'browser/templates/groupsettings.pt')

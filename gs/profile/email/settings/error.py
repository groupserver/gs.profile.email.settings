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
from __future__ import absolute_import, unicode_literals


class EmailAddressSettingsError(ValueError):
    '''An error associated with changing something to do with an email
    address.'''


class AddressExists(EmailAddressSettingsError):
    'An address already exists on the profile'


class AddressPreferred(AddressExists):
    'An address is already preferred'


class AddressExtra(AddressExists):
    'An address is already extra'


class AddressVerified(AddressExists):
    'An address is already verified'


class AddressUnverified(AddressExists):
    'An address is already unverified'


class AddressMissing(EmailAddressSettingsError):
    'An address is missing'


class RemovingOnlyPreferred(EmailAddressSettingsError):
    'The only preferred address is being removed'

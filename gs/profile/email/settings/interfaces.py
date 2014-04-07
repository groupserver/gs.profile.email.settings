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
from __future__ import unicode_literals
from zope.interface import Interface
from zope.schema import ASCII, List
from gs.profile.email.base.emailaddress import NewEmailAddress, EmailAddress


class IGSEmailSettings(Interface):

    deliveryAddresses = List(title='Addresses For Receiving Email',
        description='Addresses at which you will usually receive email from '
                      'your groups',
        value_type=EmailAddress(title='Email Address',
          description='Email address for receiving mail'),
        unique=True,
        default=[],
        required=True)

    otherAddresses = List(title='Your Other Addresses',
        description='Addresses at which you will not usually receive '
          'email from your groups, but from which you might send '
          'messages to your groups',
        value_type=EmailAddress(title='Email Address',
          description='Other email address'),
        unique=True,
        default=[],
        required=False)

    unverifiedAddresses = List(title='Your Unverified Addresses',
        description='Addresses which you have added to your profile, '
          'but which have not been determined to both (a) belong to you '
          'and (b) be currently accepting email',
        value_type=EmailAddress(title='Email Address',
          description='Unverified email address'),
        unique=True,
        default=[],
        required=False)


class IGSEmailSettingsForm(Interface):

    # --=mpj17=-- Yes, every profile must have a delivery address.
    # However, the only time that the Remove button is shown next to
    # a delivery address is when there is an Other address. The form
    # will move one out of Other and add it to Delivery.
    deliveryAddresses = ASCII(title='Addresses For Receiving Email',
        description='Addresses at which you will usually receive '
          'email from your groups',
        required=False)

    otherAddresses = ASCII(title='Other Addresses',
        description='Addresses at which you will not usually receive '
          'email from your groups, but from which you might send '
          'messages to your groups',
        required=False)

    unverifiedAddresses = ASCII(title='Unverified Addresses',
        description='Your addresses that have not be verified as working.',
        required=False)

    resendVerificationAddress = EmailAddress(
      title='Resend Verification Address',
      description='The email address you want to send a verifiation '
        'email to.',
      required=False)

    newAddress = NewEmailAddress(title='New Address',
      description='The email address you want to add.',
      required=False)

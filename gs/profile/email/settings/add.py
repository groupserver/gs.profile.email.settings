# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals, print_function
from json import dumps as to_json
from zope.formlib import form
from zope.i18n import translate
from gs.profile.email.verify.emailverificationuser import EmailVerificationUser
from gs.profile.json import email_info
from .addressform import AddressForm
from .interfaces import IAddAddress
from .utils import markup_address
from . import GSMessageFactory as _


class AddAddress(AddressForm):
    form_fields = form.Fields(IAddAddress, render_context=False)

    def __init__(self, profile, request):
        super(AddAddress, self).__init__(profile, request)
        self.label = _('add-label', 'Add an email address')

    @form.action(label=_('add-button', 'Add'), name='add', prefix='',
                 failure='handle_failure')
    def handle_add(self, action, data):
        '''Add an email address

:param action: The button that was clicked.
:param dict data: The form data.'''
        msg = self.add(data['email'])

        r = {
            'status': 0,
            'message': msg,
            'email': email_info(self.siteInfo, self.userInfo), }
        retval = to_json(r)
        return retval

    def add(self, address):
        if not address:
            raise ValueError('Address is required')

        isPreferred = (len(self.emailUser.get_delivery_addresses()) < 1)
        self.emailUser.add_address(address, isPreferred)
        self.send_verification(address)
        addr = markup_address(address)
        msg = _(
            'add-message',
            'You have <b>added</b> the email address ${address} to your profile. An email message '
            'has been sent to verify that you control the address. You must follow the '
            'instructions in the message before you can post to your groups from ${address}.',
            mapping={'address': addr})
        retval = translate(msg)
        return retval

    def send_verification(self, address):
        emailVerificationUser = EmailVerificationUser(self.context, self.userInfo, address)
        emailVerificationUser.send_verification(self.request)

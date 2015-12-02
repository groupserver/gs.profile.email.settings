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
from gs.profile.json import email_info
from .addressform import AddressForm
from .error import AddressMissing, AddressPreferred, AddressUnverified
from .interfaces import IPreferAddress
from .utils import markup_address
from . import GSMessageFactory as _


class PreferAddress(AddressForm):
    form_fields = form.Fields(IPreferAddress, render_context=False)

    def __init__(self, profile, request):
        super(PreferAddress, self).__init__(profile, request)
        self.label = 'Prefer an email address'

    @form.action(label='Prefer', name='prefer', prefix='', failure='handle_failure')
    def handle_prefer(self, action, data):
        '''Prefer an email address

:param action: The button that was clicked.
:param dict data: The form data.'''
        e = data['email'].lower()
        if (e not in self.emailUser):
            m = '{0} ({1}) lacks the address <{2}>'
            msg = m.format(self.userInfo.name, self.userInfo.id, data['email'])
            raise AddressMissing(msg)
        elif (e in self.emailUser.preferred):
            msg = 'The address <{0}> is already preferred'.format(data['email'])
            raise AddressPreferred(msg)
        elif (e in self.emailUser.unverified):
            msg = 'The address <{0}> is unverified'.format(data['email'])
            raise AddressUnverified(msg)

        msg = self.prefer(data['email'])

        r = {
            'status': 0,
            'message': msg,
            'email': email_info(self.siteInfo, self.userInfo), }
        retval = to_json(r)
        return retval

    def prefer(self, address):
        if not address:
            raise ValueError('Address is required')

        self.emailUser.set_delivery(address)
        addr = markup_address(address)
        msg = _(
            'prefer-message',
            'You have set the email address ${address} as <b>preferred</b>. You will recieve email '
            'from your groups at this address by default.',
            mapping={'address': addr})
        retval = translate(msg)
        return retval

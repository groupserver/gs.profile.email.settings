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
from .error import AddressMissing, AddressExtra, AddressUnverified
from .interfaces import IDemoteAddress
from .utils import markup_address
from . import GSMessageFactory as _


class DemoteAddress(AddressForm):
    form_fields = form.Fields(IDemoteAddress, render_context=False)

    def __init__(self, profile, request):
        super(DemoteAddress, self).__init__(profile, request)
        self.label = 'Demote an email address'

    @form.action(label='Demote', name='demote', prefix='', failure='handle_failure')
    def handle_demote(self, action, data):
        '''Demote an email address

:param action: The button that was clicked.
:param dict data: The form data.'''
        e = data['email'].lower()
        if (e not in self.emailUser):
            m = '{0} ({1}) lacks the address <{2}>'
            msg = m.format(self.userInfo.name, self.userInfo.id, data['email'])
            raise AddressMissing(msg)
        elif (e in self.emailUser.unverified):
            raise AddressUnverified(msg)
        elif (e in self.emailUser.extra):
            msg = 'The address <{0}> is not preferred'.format(data['email'])
            raise AddressExtra(msg)

        msg = self.demote(data['email'])

        r = {
            'status': 0,
            'message': msg,
            'email': email_info(self.siteInfo, self.userInfo), }
        retval = to_json(r)
        return retval

    def demote(self, address):
        if not address:
            raise ValueError('Address is required')

        self.emailUser.drop_delivery(address)
        addr = markup_address(address)
        msg = _(
            'demote-message',
            'You have set the email address ${address} as an <b>extra</b> address. You can post '
            'to your groups from this address, but by default messages will be sent to your '
            '<i>preferred</i> addresses',
            mapping={'address': addr})
        retval = translate(msg)
        return retval

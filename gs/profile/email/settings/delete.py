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
from .error import AddressMissing, RemovingOnlyPreferred
from .interfaces import IDeleteAddress
from .utils import markup_address
from . import GSMessageFactory as _


class DeleteAddress(AddressForm):
    form_fields = form.Fields(IDeleteAddress, render_context=False)

    def __init__(self, profile, request):
        super(DeleteAddress, self).__init__(profile, request)
        self.label = 'Delete an email address'

    @form.action(label='Delete', name='delete', prefix='', failure='handle_failure')
    def handle_delete(self, action, data):
        '''Delete an email address

:param action: The button that was clicked.
:param dict data: The form data.'''
        e = data['email'].lower()
        if (e not in self.emailUser):
            m = '{0} ({1}) lacks the address <{2}>'
            msg = m.format(self.userInfo.name, self.userInfo.id, data['email'])
            raise AddressMissing(msg)
        elif ((len(self.emailUser.preferred) == 1) and (e in self.emailUser.preferred)):
            msg = 'Not deleting the only preferred address <{0}>'.format(data['email'])
            raise RemovingOnlyPreferred(msg)

        msg = self.delete(data['email'])

        r = {
            'status': 0,
            'message': msg,
            'email': email_info(self.siteInfo, self.userInfo), }
        retval = to_json(r)
        return retval

    def delete(self, address):
        if not address:
            raise ValueError('Address is required')

        self.emailUser.remove_address(address)
        addr = markup_address(address)
        msg = _(
            'delete-message',
            'You have <b>removed</b> the email address ${address} from your profile.',
            mapping={'address': addr})
        retval = translate(msg)
        return retval

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
from .interfaces import IPreferAddress
from .utils import markup_address
from . import GSMessageFactory as _


class PreferAddress(AddressForm):
    form_fields = form.Fields(IPreferAddress, render_context=False)

    def __init__(self, profile, request):
        super(PreferAddress, self).__init__(profile, request)
        self.label = _('prefer-label', 'Prefer an email address')

    @form.action(label=_('prefer-button', 'Prefer'), name='prefer', prefix='',
                 failure='handle_failure')
    def handle_prefer(self, action, data):
        '''Prefer an email address

:param action: The button that was clicked.
:param dict data: The form data.'''
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

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
from .interfaces import IResendVerification
from .utils import markup_address
from . import GSMessageFactory as _


class ResendVerification(AddressForm):
    form_fields = form.Fields(IResendVerification, render_context=False)

    def __init__(self, profile, request):
        super(ResendVerification, self).__init__(profile, request)
        self.label = _('resend-label', 'Resend a email-verification message for an address')

    @form.action(label=_('resend-button', 'Resend'), name='resend', prefix='',
                 failure='handle_failure')
    def handle_resend(self, action, data):
        '''Resend an email address verification message

:param action: The button that was clicked.
:param dict data: The form data.'''
        msg = self.resend(data['email'])

        r = {
            'status': 0,
            'message': msg,
            'email': email_info(self.siteInfo, self.userInfo), }
        retval = to_json(r)
        return retval

    def resend(self, address):
        if not address:
            raise ValueError('Address is required')

        emailVerificationUser = EmailVerificationUser(self.context, self.userInfo, address)
        emailVerificationUser.send_verification(self.request)

        addr = markup_address(address)
        msg = _(
            'resend-message',
            'You have sent a new <b>verification message</b> to the email address ${address}.',
            mapping={'address': addr})
        retval = translate(msg)
        return retval
